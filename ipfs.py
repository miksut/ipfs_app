import ipfshttpclient

# prerequisites: a running instance of an IPFS daemon



if __name__ == '__main__': 
	
	# connecting to the local IPFS node and retrieving the client object
	client = ipfshttpclient.connect()
	print("IPFS daemon running on version: " + client.version()["Version"])



