import numpy as np 
from PIL import Image 
import scipy.misc
import numpy as np
import sys



def compareImages(image1_array,image2_array):
	"""Compares two images pixel-by-pixel
		:image_path1:Path to the first image
		:image_path2:Path to the second image
		:return: Number of different pixels
				in two images
	"""


	L=0
	#Calculate number of different pixels
	#divide by 255 because images are binary
	#containing two values 0 and 255
	neg_image=np.zeros(image1_array.shape)
	print(image1_array.shape)
	print('\n')
	print(image2_array.shape)
	for i in range(image1_array.shape[0]):
		for ii in range(image1_array.shape[1]):
			neg_image[i][ii]=abs(int(image1_array[i][ii])-int(image2_array[i][ii]))
			L=L+neg_image[i][ii]/255

	return L,neg_image.astype('uint8')




