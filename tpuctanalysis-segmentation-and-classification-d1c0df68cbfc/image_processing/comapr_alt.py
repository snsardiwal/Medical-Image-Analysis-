import numpy as np 
from PIL import Image
import scipy.misc
import os
import sys
import logging

from rotation import translate,rotate



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

def compare(folder_path_1,folder_path_2):
	
	file_names1=sorted(os.listdir(folder_path_1))
	file_names2=sorted(os.listdir(folder_path_2))
	dicom_file_names1 = []
	dicom_file_names2=[]
	
	for fn in file_names1:
		file_extension=fn.split('.')[-1]
		if file_extension=='png':
			dicom_file_names1.append(fn)
	dicom_file_names1=np.array(dicom_file_names1)
	
	for fn in file_names1:
		file_extension=fn.split('.')[-1]
		if file_extension=='png':
			dicom_file_names2.append(fn)
	dicom_file_names1=np.array(dicom_file_names1)
	dicom_file_names2=np.array(dicom_file_names2)
	
	for i in range(dicom_file_names1.shape[0]):
		image_path_1=os.path.join(folder_path_1,dicom_file_names1[i])
		count=-4
		while(count<9):
			ii=i+count
			if (ii>=0) and (ii < dicom_file_names2.shape[0]):
				image_path_2=os.path.join(folder_path_2,dicom_file_names2[ii])
				for x_center in range(-20,20,5):
					for y_center in range(-20,20,5):
						ipts_translate="/Users/sachin/Desktop/CT_Project/rotated_image/translate.png"
						translate_image_2=translate(image_path_2,x_center,y_center)
						translate_image_2.save(ipts_translate)	
						percent_diff=compare_images(image_path_1,ipts_translate)
						logging.basicConfig(filename='data_alt.log',level=logging.INFO)
						logging.info('%s, %s, %d, %d , %f  ',dicom_file_names1[i],dicom_file_names2[ii],x_center,y_center,percent_diff)
			count=count+1
				



folder_path_1="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130124"
folder_path_2="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130211"

compare(folder_path_1,folder_path_2)







