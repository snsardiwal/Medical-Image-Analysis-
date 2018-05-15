import numpy as np 
import scipy.ndimage
from scipy.misc.pilutil import Image
from open_dicoms import extract_dicom_slices_from_folder



image_path="/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/CT_image/000"
a=Image.open(image_path)

k=np.ones((5,5))/25

b=scipy.ndimage.filters.convolve(a,k)

b=scipy.misc.toimage(b)
b.save("/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/filter")