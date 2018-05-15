import numpy as np 
import scipy.ndimage
from scipy.misc.pilutil import Image




image_path="/Users/sachin/Desktop/CT_Project/masked_dicom_images/000.png"
a=Image.open(image_path)

k=np.ones((5,5))/25

b=scipy.ndimage.filters.median_filter(a,size=5,footprint=None,output=None,mode='reflect',cval=0.0,origin=0)

b=scipy.misc.toimage(b)
b.save("/Users/sachin/Desktop/CT_Project/masked_images_after_filter/000.png")