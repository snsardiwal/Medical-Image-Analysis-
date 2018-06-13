

from save_transform_and_image import  save_transform_and_image
from imageRegistration import  imageRegistration
import SimpleITK as sitk

imagepath1="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20121102/051.png"
imagepath2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient6/20130301/054.png"

outTx=imageRegistration(imagepath1,imagepath2)

fixed = sitk.ReadImage(imagepath1, sitk.sitkFloat32)
moving = sitk.ReadImage(imagepath2, sitk.sitkFloat32)
save_transform_and_image(outTx,fixed,moving,"049_049")
