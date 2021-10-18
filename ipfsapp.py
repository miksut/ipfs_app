import codecs
import glob
import pickle as pkl
import ipfshttpclient
import json
import numpy as np
import os
import paramiko
import re
import requests
import time


class Action:
	def __init__(self, sourcePaths):
		self.__sourcePaths = sourcePaths
		self.__timer = Timer()

	def execute(self, fileRemover, runs=1):
		performanceMeasures = np.zeros((len(self.__sourcePaths), runs))
		fileIDs = ["" for i in range(len(self.__sourcePaths))]

		for i in range(runs):

			fileRemover.execute()

			for j, path in enumerate(self.__sourcePaths):
				self.__timer.start()
				self.logic(fileIDs, j, path)
				performanceMeasures[j][i] = self.__timer.stop()

		return performanceMeasures, fileIDs

	def logic(self, fileIDs, j, path):
		raise NotImplementedError("Must override method")


class HTTPDownload(Action):
	def __init__(self, sourceDirectory, targetDirectory, removeFiles=True):
		super().__init__(self.__loadSourcePaths(sourceDirectory))
		self.__downloadDirectory = targetDirectory
		self.__fileRemover = FileRemoverOS(self.__downloadDirectory, ".txt", removeFiles)

	def __loadSourcePaths(self, sourceDirectory):
		with open(sourceDirectory, "r") as file_in:
			data = json.loads(file_in.read())
			key = list(data.keys())[0]
			return data[key]

	def logic(self, fileIDs, j, url):
		fileIDs[j] = self.__downloadDirectory + "file" + str(j+1) + ".txt"
		response = requests.get(url, allow_redirects=True)
		with open(fileIDs[j], "wb") as file_out:
			file_out.write(response.content)

	def download(self, runs=1):
		return super().execute(self.__fileRemover, runs)


class Serializer(Action):
	def __init__(self, sourceDirectory, targetDirectory, targetFormat, removeFiles=True):
		super().__init__(sourceDirectory)
		self.__storageDirectory = targetDirectory
		self.__targetFormat = targetFormat
		self.__fileRemover = FileRemoverOS(self.__storageDirectory, self.__targetFormat, removeFiles)

	def __logicJSON(self, fileIDs, j, path):
		fileIDs[j] = self.__storageDirectory + "file" + str(j+1) + self.__targetFormat
		with open(path, "r", encoding="latin1") as file_in, open(fileIDs[j], "w") as file_out:
			data = file_in.read()
			json.dump(data, file_out)

	def __logicPICKLE(self, fileIDs, j, path):
		fileIDs[j] = self.__storageDirectory + "file" + str(j+1) + self.__targetFormat
		with open(path, "r", encoding="latin1") as file_in, open(fileIDs[j], "wb") as file_out:
			data = file_in.read()
			pkl.dump(data, file_out, protocol=pkl.HIGHEST_PROTOCOL)

	def logic(self, fileIDs, j, path):
		if (self.__targetFormat == ".json"):
			self.__logicJSON(fileIDs, j, path)
		elif (self.__targetFormat == ".pkl"):
			self.__logicPICKLE(fileIDs, j, path)
		else:
			raise ValueError("Format not supported. Choose between .json and .pkl")
		
	def serialize(self, runs=1):
		return super().execute(self.__fileRemover, runs)


class Deserializer(Action):
	def __init__(self, sourceDirectory, targetDirectory, targetFormat, removeFiles=True):
		super().__init__(sourceDirectory)
		self.__storageDirectory = targetDirectory
		self.__targetFormat = targetFormat
		self.__fileRemover = FileRemoverOS(self.__storageDirectory, ".txt", removeFiles)

	def __logicJSON(self, fileIDs, j, path):
		fileIDs[j] = self.__storageDirectory + "file" + str(j+1) + "FromJSON" + ".txt"
		with open(path, "r") as file_in, open(fileIDs[j], "wb") as file_out:
			data = json.load(file_in)
			file_out.write(data.encode("latin1"))

	def __logicPICKLE(self, fileIDs, j, path):
		fileIDs[j] = self.__storageDirectory + "file" + str(j+1) + "FromPICKLE" + ".txt"
		with open(path, "rb") as file_in, open(fileIDs[j], "wb") as file_out:
			data = pkl.load(file_in)
			file_out.write(data.encode("latin1"))

	def logic(self, fileIDs, j, path):
		if (self.__targetFormat == ".json"):
			self.__logicJSON(fileIDs, j, path)
		elif (self.__targetFormat == ".pkl"):
			self.__logicPICKLE(fileIDs, j, path)
		else:
			raise ValueError("Format not supported. Choose between .json and .pkl")	

	def deserialize(self, runs=1):
		return super().execute(self.__fileRemover, runs)


class IPFSUpload(Action):
	def __init__(self, sourceDirectory, removeFiles=True):
		super().__init__(sourceDirectory)
		self.__fileRemover = FileRemoverIPFS(removeFiles)

	def logic(self, fileIDs, j, path):
		with ipfshttpclient.connect() as client:
			result = client.add(path, wrap_with_directory=True)
			directoryHash = result[1]['Hash']
			fileName = result[0]['Name']
			fileIDs[j] = [directoryHash, fileName]

	def upload(self, runs=1):
		return super().execute(self.__fileRemover, runs) 


class IPFSDownloadDist(Action):
	def __init__(self, sourceCIDs, targetDirectory, targetFormat, removeFiles=True):
		super().__init__(sourceCIDs)
		self.__storageDirectory = targetDirectory
		self.__fileRemoverIPFS = FileRemoverIPFS(removeFiles)
		self.__fileRemoverOS = FileRemoverOS(self.__storageDirectory, targetFormat, removeFiles)

	def logic(self, fileIDs, j, path):
		with ipfshttpclient.connect() as client:
			client.get(path[0] + "/" + path[1], self.__storageDirectory)
			fileIDs[j] = self.__storageDirectory + path[1]

	def download(self, runs=1):
		self.__fileRemoverOS.execute()
		return super().execute(self.__fileRemoverIPFS, runs)


class IPFSDownloadLocal(Action):
	def __init__(self, sourceCIDs, targetDirectory, targetFormat, removeFiles=True):
		super().__init__(sourceCIDs)
		self.__storageDirectory = targetDirectory
		self.__fileRemoverOS = FileRemoverOS(self.__storageDirectory, targetFormat, removeFiles)

	def logic(self, fileIDs, j, path):
		with ipfshttpclient.connect() as client:
			client.get(path[0] + "/" + path[1], self.__storageDirectory)
			fileIDs[j] = self.__storageDirectory + path[1]

	def download(self, runs=1):
		return super().execute(self.__fileRemoverOS, runs)


class IPFSClient:
	def __init__(self):
		self.__client = ipfshttpclient.connect()
		self.__confirmInstance()
		self.__nodeIP = ""

	def __confirmInstance(self):
		print("\nIPFS daemon running on version: " + self.__client.version()["Version"])
		self.__nodeIP = self.__client.id()["Addresses"][2]
		print("Node IP: " + self.__nodeIP)

	def getClient(self):
		return self.__client


class IPFSDistributor:
	def __init__(self, sourceDirectory, targetIDs):
		self.__configfilePath = sourceDirectory
		self.__targetIDs = targetIDs
		self.__client = paramiko.SSHClient()
		self.__distributedCIDs = ["" for i in range(len(self.__targetIDs))]

	def distribute(self):
		ip, user, key = self.__loadIP()
		self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.__client.connect(ip, 22, user, key, timeout=10)
		
		for i in range(len(self.__targetIDs)):
			stdin, stdout, stderr = self.__client.exec_command("ipfs get" + " " + self.__targetIDs[i][0] + "/" + self.__targetIDs[i][1])
			stdin, stdout, stderr = self.__client.exec_command("ipfs add -w" + " " + self.__targetIDs[i][1])

			storageInfos = codecs.decode(stdout.read()).split( )
			self.__distributedCIDs[i] = storageInfos[-1] + "/" + storageInfos[2]
		
		self.__client.close()
		return self.__distributedCIDs
		
	def __loadIP(self):
		with open(self.__configfilePath, "r") as file_in:
			data = json.loads(file_in.read())
			return data["ip"], data["user"], data["key"]


# Auxiliary classes
# -----------------------------------------------------------
class FileRemoverOS:
	def __init__(self, targetDirectory, targetFormat, removeFiles):
		self.__targetDirectory = targetDirectory
		self.__targetFormat = targetFormat
		self.__removeFlag = removeFiles

	def execute(self):
		if (self.__removeFlag):
			for file in glob.glob(self.__targetDirectory + "*" + self.__targetFormat):
					os.remove(file)
		else:
			pass


class FileRemoverIPFS:
	def __init__(self, removeFiles):
		self.__removeFlag = removeFiles

	def execute(self):
		if (self.__removeFlag):	
			with ipfshttpclient.connect() as client:
				pinnedContent = client.pin.ls(type='recursive')['Keys']
				for i in list(pinnedContent.keys()):
					client.pin.rm(i)
				client.repo.gc()
		else:
			pass


class Timer:
	def __init__(self):
		self.__start_time = None

	def start(self):
		if self.__start_time is not None:
			raise TimerError(f"Timer is running! Use stop() method first.")

		self.__start_time = time.perf_counter()

	def stop(self):
		if self.__start_time is None:
			raise TimerError(f"Timer is not running. Use start() method first.")

		deltaTime = time.perf_counter() - self.__start_time
		self.__start_time = None
		return deltaTime


class TimerError(Exception):
	""" Custom exception used for Timer class """


class DataStore:
	def __init__(self, fileName):
		self.__file = fileName
		self.__initFile(fileName)

	def __initFile(self, fileName):
		with open(fileName, "w") as file:
			json.dump({}, file)

	def store(self, newData):
		with open(self.__file, "r+") as file:
			data = json.load(file)
			data.update(newData)
			file.seek(0)
			json.dump(data, file)
