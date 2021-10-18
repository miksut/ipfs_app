import matplotlib.pyplot as plt
from ipfsapp import *

# Image Serialization

class Image:

    def __init__(self, runsHigh):
        self.__runsHigh = runsHigh

    def serialize(self):
        serialTimesImageJSON, filePathsSerialImageJSON = Serializer(['data/img/japari.jpg'], "data/img_serialized/",
                                                                    ".json").serialize(runs=self.__runsHigh)
        print("Image Serialization to JSON:")
        print(serialTimesImageJSON)
        print(filePathsSerialImageJSON)
        print()

        serialTimesImagePkl, filePathsSerialImagePkl = Serializer(['data/img/japari.jpg'], "data/img_serialized/",
                                                                  ".pkl").serialize(runs=self.__runsHigh)
        print("Image Serialization to Pickle:")
        print(serialTimesImagePkl)
        print(filePathsSerialImagePkl)
        print()

        # Image Storing
        uploadTimesImageJSON, ipfsIDsImageJSON = IPFSUpload(filePathsSerialImageJSON).upload(runs=self.__runsHigh)
        print("Uploading JSON Image:")
        print(uploadTimesImageJSON)
        print(ipfsIDsImageJSON)
        print()

        uploadTimesImagePkl, ipfsIDsImagePkl = IPFSUpload(filePathsSerialImagePkl, removeFiles=False).upload(runs=self.__runsHigh)
        print("Uploading PICKLE Image:")
        print(uploadTimesImagePkl)
        print(ipfsIDsImagePkl)
        print()

        combinedImageJSONTime = serialTimesImageJSON + uploadTimesImageJSON
        combinedImagePKLTime = serialTimesImagePkl + uploadTimesImagePkl
        fltJSON = combinedImageJSONTime.flatten()
        fltPKL = combinedImagePKLTime.flatten()
        fltJSON = np.around(fltJSON, decimals=3)
        fltPKL = np.around(fltPKL, decimals=3)

        # plotting figure stuff
        xx = np.arange(self.__runsHigh)
        width = 0.4
        fig, ax = plt.subplots()
        fig.set_size_inches(10,6)
        bar1 = ax.bar(xx - width / 2, fltJSON, width, label='JSON')
        bar2 = ax.bar(xx + width / 2, fltPKL, width, label='Pickle')

        ax.bar_label(bar1)
        ax.bar_label(bar2)
        plt.legend(loc='upper right')
        plt.suptitle('Algorithm Comparison for Image', fontweight='bold')
        plt.title('Serialization & Storing on IPFS node')
        plt.xlabel('Runs')
        plt.ylabel('Combined Elapsed Time [s]')
        fig.tight_layout()
        plt.savefig('pictures/image_algorithm_comparison.pdf')
        plt.show()
