import ipfshttpclient
import codecs

# prerequisites: a running instance of an IPFS daemon



if __name__ == '__main__': 
	
	# connecting to the local IPFS node and retrieving the client object
	client = ipfshttpclient.connect()
	print("IPFS daemon running on version: " + client.version()["Version"])

	# adding a file to IPFS
	retrieval_data = client.add("data/mytextfile.txt", wrap_with_directory=True)
	print(retrieval_data)

	# read the file's content via directory hash
	print((client.cat(retrieval_data[1]["Hash"] + "/" + retrieval_data[0]["Name"])).decode('UTF-16'))






