from ipfsapp import *

# prerequisites: a running instance of an IPFS daemon (<= 0.8.0)

if __name__ == '__main__': 

	# Change for adjusting the number of runs (see task description)
	runsLow = 1
	runsHigh =1

	dataStore = DataStore("eval.json")

	downloadTimesHTTP, filePathsSource = HTTPDownload("config/sourceData.json", "data/source/").download(runs=runsLow)
	dataStore.store({"DownloadTimesHTTP" : downloadTimesHTTP.tolist()})
	print("HTTP Download:")
	print(downloadTimesHTTP)
	print(filePathsSource)
	print()

	serialTimesJSON, filePathsSerialJSON = Serializer(filePathsSource, "data/serialized/", ".json").serialize(runs=runsHigh)
	dataStore.store({"SerialTimesJSON" : serialTimesJSON.tolist()})
	print("Serialization to JSON:")
	print(serialTimesJSON)
	print(filePathsSerialJSON)
	print()

	serialTimesPkl, filePathsSerialPkl = Serializer(filePathsSource, "data/serialized/", ".pkl").serialize(runs=runsHigh)
	dataStore.store({"SerialTimesPkl" : serialTimesPkl.tolist()})
	print("Serialization to Pickle:")
	print(serialTimesPkl)
	print(filePathsSerialPkl)
	print()

	uploadTimesJSON, ipfsIDsJSON = IPFSUpload(filePathsSerialJSON).upload(runs=runsHigh)
	dataStore.store({"UploadTimesJSON" : uploadTimesJSON.tolist()})
	print("Uploading JSON files:")
	print(uploadTimesJSON)
	print(ipfsIDsJSON)
	print()

	uploadTimesPkl, ipfsIDsPkl = IPFSUpload(filePathsSerialPkl, removeFiles=False).upload(runs=runsHigh)
	dataStore.store({"UploadTimesPkl" : uploadTimesPkl.tolist()})
	print("Uploading PICKLE files:")
	print(uploadTimesPkl)
	print(ipfsIDsPkl)
	print()

	downloadTimesIPFSLocalJSON, filePathsDownloadJSON = IPFSDownloadLocal(ipfsIDsJSON, "data/download/", ".json").download(runs=runsHigh)
	dataStore.store({"DownloadTimesIPFSLocalJSON" : downloadTimesIPFSLocalJSON.tolist()})
	print("Downloading JSON files from local IPFS node:")
	print(downloadTimesIPFSLocalJSON)
	print(filePathsDownloadJSON)
	print()

	downloadTimesIPFSLocalPkl, filePathsDownloadPkl = IPFSDownloadLocal(ipfsIDsPkl, "data/download/", ".pkl").download(runs=runsHigh)
	dataStore.store({"DownloadTimesIPFSLocalPkl" : downloadTimesIPFSLocalPkl.tolist()})
	print("Downloading PICKLE files from local IPFS node:")
	print(downloadTimesIPFSLocalPkl)
	print(filePathsDownloadPkl)
	print()

	deserialTimesJSON, filePathsDeserialJSON = Deserializer(filePathsDownloadJSON, "data/deserialized/", ".json").deserialize(runs=runsHigh)
	dataStore.store({"DeserialTimesJSON" : deserialTimesJSON.tolist()})
	print("Deserialization from JSON:")
	print(deserialTimesJSON)
	print(filePathsDeserialJSON)
	print()

	deserialTimesPkl, filePathsDeserialPkl = Deserializer(filePathsDownloadPkl, "data/deserialized/", ".pkl", removeFiles=False).deserialize(runs=runsHigh)
	dataStore.store({"DeserialTimesPkl" : deserialTimesPkl.tolist()})
	print("Deserialization from PICKLE:")
	print(deserialTimesPkl)
	print(filePathsDeserialPkl)
	print()
