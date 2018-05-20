import numpy as np 
from PIL import Image
import scipy.misc






def compare_images(image_path_1,image_path_2):
	image1=Image.open(image_path_1).convert('L')
	image2=Image.open(image_path_2).convert('L')

	image1_array=scipy.misc.fromimage(image1)
	image2_array=scipy.misc.fromimage(image2)

	pix_diff=0
	for i in range(image1_array.shape[0]):
		for ii in range(image1_array.shape[1]):
			if image1_array[i][ii]!=image2_array[i][ii]:
				pix_diff=pix_diff+1

	total_pixel=image1_array.shape[0]*image1_array.shape[1]
	percent_diff=(float(pix_diff)/total_pixel)*100

	return percent_diff


image_path_1="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130124/027.png"
image_path_2="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130211/040.png"

pix_diff=compare_images(image_path_1,image_path_2)
print(pix_diff)





