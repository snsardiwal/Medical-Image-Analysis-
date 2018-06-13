import numpy as np

from sklearn.cluster import KMeans
from skimage import morphology
from skimage import measure
import sys
import cv2
from PIL import Image
from skimage.filters.thresholding import threshold_otsu
sys.path.insert(0, "/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
from config import lungs_segmentation as ls_conf


def get_lungs_masks_for_slices(dicom_slices_array):
    """
    Performs the slices segmentation and returns a lungs mask for all slices
    :param dicom_slices_array: ndarray of original dicom slices pixel data
    :return: ndarray of dicom slices pixel data where values are equal to 1 or 0:
     1 is the pixel belonging to lungs, 0 is the pixel belonging to other structures
    """
    segmented_slices = []
    for s in dicom_slices_array:
        segmented_slices.append(get_lungs_mask_for_slice(s))

    return np.stack(segmented_slices)


def get_lungs_mask_for_slice(slice_array):
    """
    Performs the slices segmentation and returns a lungs mask
    :param slice_array: ndarray of a dicom slice data
    :return: ndarray of dicom slice data where values are equal to 1 or 0:
     1 is the pixel belonging to lungs, 0 is the pixel belonging to other structures
    """
    rows_num = slice_array.shape[0]
    cols_num = slice_array.shape[1]

    thres=threshold_otsu(slice_array)

    slice_array[slice_array>thres]=255
    slice_array[slice_array<=thres]=0

    # Make erosion and dilation to smooth noises
    ef_size = ls_conf['erosion_filter_size']
    df_size = ls_conf['dilation_filter_size']
    eroded_slice = morphology.erosion(slice_array, np.ones([ef_size, ef_size]))
    dilated_slice = morphology.dilation(eroded_slice, np.ones([df_size, df_size]))

    im=Image.fromarray(dilated_slice)
    im.save("010.png")

    # Find regions which are fit to the estimated position of lungs
    labels = measure.label(dilated_slice)
    regions = measure.regionprops(labels)
    fit_labels = []
    for prop in regions:
        bbox = prop.bbox
        if bbox[2] - bbox[0] < rows_num / 10 * 9 and \
           bbox[3] - bbox[1] < cols_num / 10 * 9 and \
           bbox[0] > rows_num / 5 and \
           bbox[2] < cols_num / 5 * 4:
            fit_labels.append(prop.label)

    # Creating lungs mask
    lungs_mask = np.ndarray([rows_num, cols_num], dtype=np.uint8)
    lungs_mask[:] = 0
    for lb in fit_labels:
        lungs_mask = lungs_mask + np.where(labels == lb, 1, 0)
    lungs_mask = morphology.dilation(lungs_mask, np.ones([df_size, df_size]))

    return lungs_mask


image_path = "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient1/time1/befNorm/035.png"
preset_slice = "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient1/time1/aftNorm/035.png"

image=Image.open(image_path).convert('L')
image=np.array(image)
mask=get_lungs_mask_for_slice(image)

preset_slice=cv2.imread(preset_slice,0)
preset_slice=np.array(preset_slice)

im=(preset_slice*mask).astype(np.uint8)
im=Image.fromarray(im)
im.save("009.png")

