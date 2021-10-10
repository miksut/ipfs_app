import ipfshttpclient
import numpy as np
import json
import os
import requests
import time


class DownloadManagerHTTP:
	def __init__(self, sourcePaths, downloadDir):
		self.__sourcePaths = self.__loadSourcePaths(sourcePaths)
		self.__downloadDir = downloadDir
		self.__timer = Timer()

	def __loadSourcePaths(self, sourcePaths):
		with open(sourcePaths, "r") as file_in:
			paths = json.loads(file_in.read())
			key = list(paths.keys())[0]
			return paths[key]

	def downloadFiles(self, runs=1):
		downloadTimes = np.zeros((len(self.__sourcePaths), runs))
		print(downloadTimes)

		for i in range(runs):

			for file in os.scandir(self.__downloadDir):
				os.remove(file.path)

			for j, url in enumerate(self.__sourcePaths):
				self.__timer.start()
				response = requests.get(url, allow_redirects=True)
				with open(self.__downloadDir + "file" + str(j+1) + ".txt", "wb") as file_out:
					file_out.write(response.content)
				downloadTimes[j][i] = self.__timer.stop()

		return downloadTimes


class IPFSManager:
	def __init__(self):
		self.client = ipfshttpclient.connect()
		self.__confirmInstance()

	def __confirmInstance(self):
		print("\nIPFS daemon running on version: " + self.client.version()["Version"])
		print("Node IP: " + self.client.id()["Addresses"][2])


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