import scipy.misc
from PIL import Image
import numpy as np

import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage.filters.thresholding import threshold_otsu
from skimage import morphology
from skimage import measure
from config import lungs_segmentation as ls_conf



def get_lung_mask_from_slices(dicom_slices_array):

	segmented_slices = []

	for s in dicom_slices_array:
		segmented_slices.append(get_lung_mask_from_slice(s))

	return np.stack(segmented_slices)




def get_lung_mask_from_slice(slice_array):

	
	thres=threshold_otsu(slice_array)


	thresholded_array=np.where(slice_array>thres,0,255).astype('uint8')

	
	ef_size = ls_conf['erosion_filter_size']
	df_size=ls_conf['dilation_filter_size']

	eroded_slice=morphology.erosion(thresholded_array,np.ones([ef_size,ef_size]))
	dilated_slice=morphology.dilation(eroded_slice,np.ones([df_size,df_size]))

	labels=measure.label(dilated_slice)
	regions=measure.regionprops(labels)


	#Visualization
	im=Image.fromarray(dilated_array)
	im.save("011.png")


image_path = "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient1/time1/aftNorm/024.png"



"""

fig,ax= plt.subplots(ncols=1,nrows=1,figsize=(10,10))
ax.imshow(labels,cmap='YlOrRd')
im=Image.fromarray(dilated_slice)
im.save("011.png")
"""