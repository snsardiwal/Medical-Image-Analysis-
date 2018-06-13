
import os
import sys
from PIL import Image
import numpy as np
from image_processing.compareMask import *
from image_processing.registration_displacement import *
from dicom_saving.save_dicoms import *


folder_path1="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20121102/049.png"
folder_path2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20130301/050.png"

im1=np.array(Image.open(folder_path1))
im2=np.array(Image.open(folder_path2))

im2A=imageRegistration(folder_path1,folder_path2)


LB,negB=compareImages(im1,im2)
negB=Image.fromarray(negB)
negB.show()

LA,negA=compareImages(im1,im2A)
negA=Image.fromarray(negA)
negA.show()

print("%d %d" % (LB,LA))


