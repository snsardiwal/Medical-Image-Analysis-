
import os
import sys
import scipy.misc
from PIL import Image
from imageRegistration import *
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
from dicom_saving.save_dicoms import *
from  listFileNames import *
from compare import *
folder_path1="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20121102/049.png"
folder_path2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20130301/049.png"
#folder_path_to_save="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/Patient1/"
#neg_Image=imageRegistration(folder_path1,folder_path2)
#neg_Image=Image.fromarray(neg_Image.astype('uint8'),'RGB')
#print(neg_Image.shape)
#neg_Image.show()
#neg_Image.save(folder_path_to_save)

#im1Reg,im2Reg,neg_Image=imageRegistrationFromFolder(folder_path1,folder_path2)
im1,im2,cim=imageRegistration(folder_path1,folder_path2)

print(np.amax(im1))
print(np.amax(im2))

im1bef=Image.open(folder_path1)
im2bef=Image.open(folder_path2)

im1bef=np.array(im1bef)
im2bef=np.array(im2bef)

#negImageBef,Lbef=compare_images_image(im1bef,im2bef)
#negImageAft,Laft=compare_images_image(im1,im2)

#Lbef=manhattan_distance(im1bef,im2bef)
#Laft=manhattan_distance(im1,im2)

print("%d %d" %(Lbef,Laft))



#Converting arrays into images
#im1Reg=Image.fromarray(im1Reg.astype('uint8'),'RGB')
#im2Reg=Image.fromarray(im2Reg.astype('uint8'),'RGB')
#neg_Image=Image.fromarray(neg_Image.astype('uint8','RGB'))

#Save negative images
#save_slices_as_images(negImage,folder_path_to_save)

