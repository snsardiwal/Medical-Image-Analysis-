import numpy as np 
import scipy.ndimage
from scipy.misc.pilutil import Image
import scipy.misc

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



image_path="/Users/sachin/Desktop/CT_Project/bone_mask/patient1/20130211/042.png"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130211/042.png"
median_filter(image_path,folder_path_to_save)



