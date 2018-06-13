import cv2
import numpy as np
import matplotlib 
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from PIL import Image 

from dicom_data_working import extract_dicom_slices_from_folder,convert_slices_to_preset

def hist(image_path):

	image=cv2.imread(image_path,0)
	image=np.array(image)
	hist=plt.hist(image.ravel(),100,[0,100])
	plt.show()

def histNorm(image_path):

	image=cv2.imread(image_path,0)
	image=np.array(image)
	mean=np.mean(image)
	std=np.std(image)
	image=(image-mean)/std
	hist=plt.hist(image.ravel(),3,[0,3])
	plt.show()
def mask(image_path):
	image=cv2.imread(image_path,0)
	image=np.array(image,np.uint8)
	image[image<=1]=0
	image[image>1]=255

	return image

def segment(dicom_path,preset_path):
	
	image=cv2.imread(dicom_path,0)
	m=mask(dicom_path)

	preset_slice=cv2.imread(preset_path,0)
	preset_slice=np.array(preset_slice,np.uint8)


	modImage=(m*preset_slice).astype(np.uint8)
	modImage=Image.fromarray(modImage)
	modImage.save("000.png")


dicom_path = "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient3/time1/aftNorm/062.png"
preset_path =  "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient3/time1/aftNorm/062.png"
#segment(dicom_path,preset_path)


hist(dicom_path)
