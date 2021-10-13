import codecs
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
	def __init__(self, sourceDirectory, targetDirectory):
		super().__init__(self.__loadSourcePaths(sourceDirectory))
		self.__downloadDirectory = targetDirectory
		self.__fileRemover = FileRemoverOS(self.__downloadDirectory)

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
	def __init__(self, sourceDirectory, targetDirectory):
		super().__init__(sourceDirectory)
		self.__storageDirectory = targetDirectory
		self.__fileRemover = FileRemoverOS(self.__storageDirectory)

	def logic(self, fileIDs, j, path):
		fileIDs[j] = self.__storageDirectory + "file" + str(j+1) +".json"
		with open(path, "r", encoding="latin1") as file_in, open(fileIDs[j], "w") as file_out:
			data = file_in.readlines()
			json.dump(data, file_out)

	def serialize(self, runs=1):
		return super().execute(self.__fileRemover, runs)


class IPFSUpload(Action):
	def __init__(self, sourceDirectory, ipfsClient):
		super().__init__(sourceDirectory)
		self.__ipfsClient = ipfsClient
		self.__fileRemover = FileRemoverIPFS(self.__ipfsClient)

	def logic(self, fileIDs, j, path):
		result = self.__ipfsClient.add(path, wrap_with_directory=True)
		directoryHash = result[1]['Hash']
		fileName = result[0]['Name']
		fileIDs[j] = [directoryHash, fileName]

	def upload(self, runs=1):
		return super().execute(self.__fileRemover, runs) 


class IPFSDownload(Action):
	def __init__(self, sourceCIDs, targetDirectory, ipfsClient):
		super().__init__(sourceCIDs)
		self.__storageDirectory = targetDirectory
		self.__ipfsClient = ipfsClient
		self.__fileRemoverIPFS = FileRemoverIPFS(self.__ipfsClient)
		self.__fileRemoverOS = FileRemoverOS(self.__storageDirectory)

	def logic(self, fileIDs, j, path):
		self.__ipfsClient.get(path, self.__storageDirectory)
		fileIDs[j] = self.__storageDirectory + path.split("/")[-1]

	def download(self, runs=1):
		self.__fileRemoverOS.execute()
		return super().execute(self.__fileRemoverIPFS, runs)


class IPFSClient:
	def __init__(self):
		self.__client = ipfshttpclient.connect()
		self.__confirmInstance()

	def __confirmInstance(self):
		print("\nIPFS daemon running on version: " + self.__client.version()["Version"])
		print("Node IP: " + self.__client.id()["Addresses"][2])

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
	def __init__(self, targetDirectory):
		self.__targetDirectory = targetDirectory

	def execute(self):
		for file in os.scandir(self.__targetDirectory):
				os.remove(file.path)


class FileRemoverIPFS:
	def __init__(self, ipfsClient):
		self.__ipfsClient = ipfsClient

	def execute(self):
		pinnedContent = self.__ipfsClient.pin.ls(type='recursive')['Keys']

		for i in list(pinnedContent.keys()):
			self.__ipfsClient.pin.rm(i)
		self.__ipfsClient.repo.gc()


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