from ipfsapp import *
import getpass

# prerequisites: a running instance of an IPFS daemon (<= 0.8.0)

if __name__ == '__main__': 
	client = IPFSClient().getClient()

	downloadTimesHTTP, filePathsSource = HTTPDownload("config/sourceData.json", "data/source/").download(runs=1)
	print(downloadTimesHTTP)
	print(filePathsSource)

	serializationTimes, filePathsSerial = Serializer(filePathsSource, "data/serialized/").serialize(runs=1)
	print(serializationTimes)
	print(filePathsSerial)

	uploadTimes, ipfsIDs = IPFSUpload(filePathsSerial, client).upload(runs=1)
	print(uploadTimes)
	print(ipfsIDs)

	# currently an undetected bug in the IPFSDistributor class, paths are hardcoded for the moment
	#distributedIDs = IPFSDistributor("config/ssh.json", ipfsIDs).distribute()
	
	distributedIDs = ["QmQtUcq2ddiw4XmUs88WP5hUyA1DSh2GPQzsdDfyrdPx5G/file1.json"]
	#distributedIDs = ["QmQtUcq2ddiw4XmUs88WP5hUyA1DSh2GPQzsdDfyrdPx5G/file1.json", "QmP8gDsjjwqZuVEYW4WRaTVzGMbjraRrdVHfhk2mqAAtg6/file2.json"]

	downloadTimesIPFS, filePathsDownload = IPFSDownload(distributedIDs, "data/download/", client).download(runs=1)
	print(downloadTimesIPFS)
	print(filePathsDownload)
	
