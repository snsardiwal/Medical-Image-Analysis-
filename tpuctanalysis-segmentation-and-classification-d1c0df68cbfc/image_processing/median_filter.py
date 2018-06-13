import numpy as np 
import scipy.ndimage
from scipy.misc.pilutil import Image
import scipy.misc
import os
from image_processing.listFileNamesInFolder import *

def median_filter(image_path):
	"""
	Applies median filter on image and saves it in a folder
	:image_path: path to the image
	:folder_path_to_save: Path to the folder to save the image
	"""
	a=Image.open(image_path)
	b=scipy.ndimage.filters.median_filter(a,size=3,footprint=None,output=None,mode='reflect',cval=0.0,origin=0)
	#b=scipy.misc.toimage(b)
	#b.save(folder_path_to_save)
	return b 


def applyMedianFilterFolder(folder_path,folder_path_to_save):

	filenames=listFileNames(folder_path)

	

	for file in filenames:
		image_path=os.path.join(folder_path,file)
		image_path_to_save=os.path.join(folder_path_to_save,file)
		image=median_filter(image_path)
		image=scipy.misc.toimage(image)
		image.save(image_path_to_save)




