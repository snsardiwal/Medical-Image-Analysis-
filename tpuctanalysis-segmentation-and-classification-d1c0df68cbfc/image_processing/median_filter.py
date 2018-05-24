import numpy as np 
import scipy.ndimage
from scipy.misc.pilutil import Image
import scipy.misc
import os
def median_filter(image_path,folder_path_to_save):
	"""
	Applies median filter on image and saves it in a folder
	:image_path: path to the image
	:folder_path_to_save: Path to the folder to save the image
	"""
	a=Image.open(image_path).convert('L')
	b=scipy.ndimage.filters.median_filter(a,size=3,footprint=None,output=None,mode='reflect',cval=0.0,origin=0)
	b=scipy.misc.toimage(b)
	b.save(folder_path_to_save)



folder_path="/Users/sachin/Desktop/CT_Project/bone_mask/patient4/20110222"
folder_path1="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient4/20110222"

#Read file names from folder
file_names=sorted(os.listdir(folder_path))

dicom_file_names = []

for fn in file_names:
	file_extension=fn.split('.')[-1]
	if file_extension=='png':
		dicom_file_names.append(fn)
	
	

for file in dicom_file_names:
	image_path=os.path.join(folder_path,file)
	folder_path_to_save=os.path.join(folder_path1,file)
	median_filter(image_path,folder_path_to_save)



