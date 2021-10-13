from ipfsapp import *
import getpass

# prerequisites: a running instance of an IPFS daemon (<= 0.8.0)

if __name__ == '__main__': 
	client = IPFSClient().getClient()

	downloadTimes, filePathsSource = HTTPDownload("config/sourceData.json", "data/source/").download(runs=1)
	print(downloadTimes)
	print(filePathsSource)

	serializationTimes, filePathsSerial = Serializer(filePathsSource, "data/serialized/").serialize(runs=1)
	print(serializationTimes)
	print(filePathsSerial)

	uploadTimes, ipfsIDs = IPFSUpload(filePathsSerial, client).upload(runs=1)
	print(uploadTimes)

	distributedIDs = IPFSDistributor("config/ssh.json", ipfsIDs).distribute()
	print(distributedIDs)
