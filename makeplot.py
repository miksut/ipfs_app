import matplotlib.pyplot as plt
import json
import numpy as np

def make_plot(title, filename, data_set1, data_set1_label, data_set2, data_set2_label):
	""" function to save a plot into a file with two datasets"""

	if len(data_set1) != len(data_set2):
		raise IndexError('Datasets are not of the same size.')

	x = np.arange(len(data_set1))
	plt.plot(x, data_set1, '-rx', label=data_set1_label)
	plt.plot(x, data_set2, '-bx', label=data_set2_label)
	plt.ylabel('elapsed time [s]')
	plt.xlabel('run')
	plt.suptitle(title)
	plt.legend()

	print(f'Saving plot to {filename}')
	plt.savefig(filename)
	plt.show()



with open('results/evaluation.json') as f:
	data = json.load(f)

	data['TotalJSON'] = {}
	data['TotalJSON'][0] = np.add(data['SerialTimesJSON'][0], data['UploadTimesJSON'][0])
	data['TotalJSON'][1] = np.add(data['SerialTimesJSON'][1], data['UploadTimesJSON'][1])

	data['TotalPKL'] = {}
	data['TotalPKL'][0] = np.add(data['SerialTimesPkl'][0],data['SerialTimesPkl'][0])
	data['TotalPKL'][1] = np.add(data['SerialTimesPkl'][1] , data['SerialTimesPkl'][1])

	data['TotalDownloadJSON'] = {}
	data['TotalDownloadJSON'][0] = np.add(data["DownloadTimesIPFSLocalJSON"][0], data["DeserialTimesJSON"][0])
	data['TotalDownloadJSON'][1] = np.add(data["DownloadTimesIPFSLocalJSON"][1], data["DeserialTimesJSON"][1])

	data['TotalDownloadPKL'] = {}
	data['TotalDownloadPKL'][0] = np.add(data["DownloadTimesIPFSLocalPkl"][0], data["DeserialTimesPkl"][0])
	data['TotalDownloadPKL'][1] = np.add(data["DownloadTimesIPFSLocalPkl"][1], data["DeserialTimesPkl"][1])

	make_plot('Serialize and store (1 MB)', 'pictures/serialization1mb.jpg', data['TotalJSON'][0], 'json', data['TotalPKL'][0], 'pickle')
	make_plot('Serialize and store (100 MB)', 'pictures/serialization100mb.jpg', data['TotalJSON'][1], 'json', data['TotalPKL'][1], 'pickle')
	make_plot('Retrieve and deserialize (1 MB)', 'pictures/deserialization1mb.jpg', data['TotalDownloadJSON'][0], 'json', data['TotalDownloadPKL'][0], 'pickle')
	make_plot('Retrieve and deserialize (100 MB)', 'pictures/deserialization100mb.jpg', data['TotalDownloadJSON'][1], 'json', data['TotalDownloadPKL'][1], 'pickle')