import ipfshttpclient
import json
import time

# prerequisites: a running instance of an IPFS daemon (<= 0.8.0)

if __name__ == '__main__': 
	
	# connecting to the local IPFS node
	client = ipfshttpclient.connect()
	print("\nIPFS daemon running on version: " + client.version()["Version"])
	print("\nNode IP: " + client.id()["Addresses"][2])

	# serializing the data to be stored
	t0 = time.perf_counter()

	with open("data/1mb.txt", "r", encoding="latin1") as file_in, open("data/1mb.json", "w") as file_out:
		data = file_in.readlines()
		json.dump(data, file_out)

	t1 = time.perf_counter()
	print(f"Time to serialize: {t1-t0:0.4f} seconds")

	# adding a file to IPFS
	retrieval_data = client.add("data/1mb.json", wrap_with_directory=True)
	print(retrieval_data)

	# read the file's content via directory hash
	#print((client.cat(retrieval_data[1]["Hash"] + "/" + retrieval_data[0]["Name"])).decode('UTF-16'))

	# download file from ipfs
	t2 = time.perf_counter()
	client.get(retrieval_data[1]["Hash"] + "/" + retrieval_data[0]["Name"], "tmp/")
	t3 = time.perf_counter()
	print(f"Time to download from local IPFS node: {t3-t2:0.04f} seconds")







