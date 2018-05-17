import numpy as np 
from PIL import Image
import scipy.misc
from skimage import transform

image_path="/Users/sachin/Desktop/CT_Project/bone_mask_after_median_filter/patient1/20130124/027.png"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/rotated_image/027.png"


x_sum=0
y_sum=0
count=0

def rotate(image_path,angle):
	image=Image.open(image_path).convert('L')
	image_array=scipy.misc.fromimage(image)
	x_sum=0
	y_sum=0
	count=0
	for i in range(image_array.shape[0]):
		for ii in range(image_array.shape[1]):
			if image_array[i][ii]==255:
				x_sum+=i
				y_sum+=ii
				count+=1

	x_center=x_sum/count
	y_center=y_sum/count

	rotated_image=transform.rotate(image_array,angle,center=(x_center,y_center))
	rotated_image=scipy.misc.toimage(rotated_image)
	return rotated_image

def translate(image_path,x_shift,y_shift):
	image=Image.open(image_path).convert('L')
	image_array=scipy.misc.fromimage(image)
	image=image.transform(image.size,Image.AFFINE,(1,0,x_shift,0,1,y_shift))
	return image

rotated_image=rotate(image_path,10)
rotated_image=translate(image_path,0,50)
rotated_image.save(folder_path_to_save)

	



