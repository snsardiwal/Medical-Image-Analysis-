import os
import sys
import scipy.misc
from PIL import Image
from imageRegistration import *
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
from dicom_saving.save_dicoms import *
from  listFileNames import *


folder_path1="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/time1/045.png"
folder_path2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/time2/045.png"
im1,im2,im3=imageRegistration(folder_path1,folder_path2)

#im1=Image.fromarray(im1)
#im2=Image.fromarray(im2)
#im3=Image.fromarray(nda)


print(im3.shape)

im1=Image.fromarray(im1).save('im1.png')
im2=Image.fromarray(im2).save('im2.png')
im3=Image.fromarray(im3).save('im3.png')