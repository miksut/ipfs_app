from ipfsapp import *
from image import *

# prerequisites: a running instance of an IPFS daemon (<= 0.8.0)

if __name__ == '__main__': 

	# Change for adjusting the number of runs (see task description)
	runsLow = 1
	runsHigh = 5

	downloadTimesHTTP, filePathsSource = HTTPDownload("config/sourceDataOriginal.json", "data/source/").download(runs=runsLow)
	print("HTTP Download:")
	print(downloadTimesHTTP)
	print(filePathsSource)
	print()

	serialTimesJSON, filePathsSerialJSON = Serializer(filePathsSource, "data/serialized/", ".json").serialize(runs=runsHigh)
	print("Serialization to JSON:")
	print(serialTimesJSON)
	print(filePathsSerialJSON)
	print()

	serialTimesPkl, filePathsSerialPkl = Serializer(filePathsSource, "data/serialized/", ".pkl").serialize(runs=runsHigh)
	print("Serialization to Pickle:")
	print(serialTimesPkl)
	print(filePathsSerialPkl)
	print()

	uploadTimesJSON, ipfsIDsJSON = IPFSUpload(filePathsSerialJSON).upload(runs=runsHigh)
	print("Uploading JSON files:")
	print(uploadTimesJSON)
	print(ipfsIDsJSON)
	print()

	uploadTimesPkl, ipfsIDsPkl = IPFSUpload(filePathsSerialPkl, removeFiles=False).upload(runs=runsHigh)
	print("Uploading PICKLE files:")
	print(uploadTimesPkl)
	print(ipfsIDsPkl)
	print()

	downloadTimesIPFSLocalJSON, filePathsDownloadJSON = IPFSDownloadLocal(ipfsIDsJSON, "data/download/", ".json").download(runs=runsHigh)
	print("Downloading JSON files from local IPFS node:")
	print(downloadTimesIPFSLocalJSON)
	print(filePathsDownloadJSON)
	print()

	downloadTimesIPFSLocalPkl, filePathsDownloadPkl = IPFSDownloadLocal(ipfsIDsPkl, "data/download/", ".pkl").download(runs=runsHigh)
	print("Downloading PICKLE files from local IPFS node:")
	print(downloadTimesIPFSLocalPkl)
	print(filePathsDownloadPkl)
	print()

		# TODO: change first argument (-> donwload directory)
	deserialTimesJSON, filePathsDeserialJSON = Deserializer(filePathsDownloadJSON, "data/deserialized/", ".json").deserialize(runs=runsHigh)
	print("Deserialization from JSON:")
	print(deserialTimesJSON)
	print(filePathsDeserialJSON)
	print()

	# TODO: change first argument (-> donwload directory)
	deserialTimesPkl, filePathsDeserialPkl = Deserializer(filePathsDownloadPkl, "data/deserialized/", ".pkl", removeFiles=False).deserialize(runs=runsHigh)
	print("Deserialization from PICKLE:")
	print(deserialTimesPkl)
	print(filePathsDeserialPkl)
	print()

	# Image Serialization
	imageHandler = Image(runsHigh=runsHigh).serialize()


"""
	#distributedIDs = ["QmQtUcq2ddiw4XmUs88WP5hUyA1DSh2GPQzsdDfyrdPx5G/file1.json"]
	distributedIDs = ["QmQtUcq2ddiw4XmUs88WP5hUyA1DSh2GPQzsdDfyrdPx5G/file1.json", "QmP8gDsjjwqZuVEYW4WRaTVzGMbjraRrdVHfhk2mqAAtg6/file2.json"]

"""