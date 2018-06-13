import numpy as np
import os
import sys
import glob
from PIL import Image

sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
from config import radiology_tissue_options as rt_opt
from config import dicom_options as d_opt



def get_bone_mask(dicom_slices):
    """
    Returns a mask based on the tissue density from dicom data where
    0 corresponds to tissues which density is lower than bone
    1 corresponds to tissues which density is equal or higher than bone
    :param dicom_slices: ndarray of dicom slices data
    :return: ndarray of masks for slices
    """
    mask = np.copy(dicom_slices)
    left = rt_opt['bone_dicom']['left']
    right = rt_opt['bone_dicom']['right']

    mask[mask < left] = 0
    mask[mask > right] = 0
    mask[mask != 0] = 1

    return mask


def save_bone_mask_as_images(mask):
    
    for i in range(mask.shape[0]):
        mask_image=Image.fromarray(mask[i])
        mask_image_path=os.path.join(folder_path_to_save,
                                    d_opt['filename_pattern'].format(i))
        mask_image.save(mask_image_path)


