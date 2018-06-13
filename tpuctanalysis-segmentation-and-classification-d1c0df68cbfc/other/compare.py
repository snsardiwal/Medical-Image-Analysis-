import numpy as np 
from PIL import Image
import scipy.misc
import os
import sys
import logging


def compare_images(image1_array,image2_array):
	"""Compares two images pixel-by-pixel
		:image_path1:Path to the first image
		:image_path2:Path to the second image
		:return: Number of different pixels
				in two images
	"""
	#read image1 and image2 and convert them to grayscale	
	image1=Image.open(image_path1)
	image2=Image.open(image_path2)

	#convert images to array
	image1_array=scipy.misc.fromimage(image1)
	image2_array=scipy.misc.fromimage(image2)

	L=0
	#Calculate number of different pixels
	#divide by 255 because images are binary
	#containing two values 0 and 255
	neg_image=np.zeros(image1_array.shape)
	for i in range(image1_array.shape[0]):
		for ii in range(image1_array.shape[1]):
			neg_image[i][ii]=abs(int(image1_array[i][ii])-int(image2_array[i][ii]))
			print(neg_image[i][ii])
			print('\n')
			L=L+neg_image[i][ii]

	return neg_image, L


def compare_after_transformation(folder_path1,folder_path2):
	"""Makes some transformation(translation and rotational) 
		on images in second folder and compares it to images
		in first folder to find Manhattan norm
		:folder_path1: Path to directory containing images at initial time
		:folder_path2: Path to directory containing images at later time
	"""
	#Read file names from folder
	file_names1=sorted(os.listdir(folder_path1))
	file_names2=sorted(os.listdir(folder_path2))
	dicom_file_names1 = []
	dicom_file_names2=[]
	for fn in file_names1:
		file_extension=fn.split('.')[-1]
		if file_extension=='png':
			dicom_file_names1.append(fn)
	
	for fn in file_names2:
		file_extension=fn.split('.')[-1]
		if file_extension=='png':
			dicom_file_names2.append(fn)
	
	#converted into numpy array
	dicom_file_names1=np.array(dicom_file_names1)
	dicom_file_names2=np.array(dicom_file_names2)
	
	"""transforms and compares 9 images from folder2 with 
	   every image in folder1 and prints the manhattan norm
	   :ipts_translate: Path of image2 after applying transformation
	"""
	
	for i in range(40,dicom_file_names1.shape[0]):
		image_path1=os.path.join(folder_path1,dicom_file_names1[i])
		count=-4
		while(count<5):
			ii=i+count
			if (ii>=0) and (ii < dicom_file_names2.shape[0]):
				image_path2=os.path.join(folder_path2,dicom_file_names2[ii])
				for x_center in range(-20,20,5):
					for y_center in range(-20,20,5):
						
						ipts_translate="/Users/sachin/Desktop/CT_Project/rotated_image/translate2.png"
						image2_after_trans=translate(image_path2,x_center,y_center)
						image2_after_trans.save(ipts_translate)	
						#compare image1 with transformed image2
						neg_image,L=compare_images(image_path1,ipts_translate)
						
						filename="%s_%s_%s_%s"%(i,ii,x_center,y_center) + ".png"
						path_to_save="/Users/sachin/Desktop/CT_Project/Neg_images/patient2"
						neg_image=scipy.misc.toimage(neg_image)
						#print(filename)
						neg_image.save(os.path.join(path_to_save,filename))
						
						output="%s %s %d %d %d" % (dicom_file_names1[i],dicom_file_names2[ii],x_center,y_center,L)	
						with open('patient2.log','a') as f:
							f.write(output)
							f.write('\n')
						
			count=count+1

		

#def main(folder_path1,folder_path2):

#	compare_after_transformation(folder_path1,folder_path2)

#if __name__=='__main__':

#	if(len(sys.argv)!=3):
#		print('Provide path to <folder1> <folder2>')
#		sys.exit(-1)


	#main(sys.argv[1],sys.argv[2])
#folder_path1="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient2/20110908"
#folder_path2="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient2/20111121"
#compare_after_transformation(folder_path1,folder_path2)






