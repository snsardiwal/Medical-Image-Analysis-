import numpy as np 
from PIL import Image
import os



def crop_image(image_path):
	a=Image.open(image_path)
	a=a.crop((0,0,512,430))
	return a


folder_path="/Users/sachin/Desktop/CT_Project/masked_dicom_images/patient1/20130124/"
#file_names=sorted(os.listdir(folder_path))
#dicom_file_names=[]
#for fn in file_names:
#	file_extension=fn.split('.')[-1]
#	if file_extension in d_opt['extensions']:
#		dicom_file_names.append(fn)

file_names = sorted(os.listdir(folder_path))
dicom_file_names = []
for fn in file_names:
    file_extension = fn.split('.')[-1]
    if file_extension=="png":
        dicom_file_names.append(fn)

folder_path_to_save="/Users/sachin/Desktop/CT_Project/croped_images/patient1/20130124"

for fn in dicom_file_names:
	image_path=os.path.join(folder_path,fn)
	image_path_to_save=os.path.join(folder_path_to_save,fn)
	image=crop_image(image_path)
	image.save(image_path_to_save)

