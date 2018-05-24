import numpy as np
import os
import sys
import glob

sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/dicom_data_working")
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")

from PIL import Image
from config import radiology_tissue_options as rt_opt
from config import dicom_options as d_opt
from open_dicoms import extract_dicom_slices_from_folder


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
    mask[mask != 0] = 255

    return mask


def save_bone_mask_as_images(mask):
    
    for i in range(mask.shape[0]):
        mask_image=Image.fromarray(mask[i])
        mask_image_path=os.path.join(folder_path_to_save,
                                    d_opt['filename_pattern'].format(i))
        mask_image.save(mask_image_path)

folder_path="/Users/sachin/Desktop/CT_Project/datasets/clinical_records_20180207_073213_97/97/CT/20110222"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/masked_dicom_images/Patient4/20110222"

#dicom_slices=extract_dicom_slices_from_folder(folder_path,0,0)
#mask=get_bone_mask(dicom_slices)
#save_bone_mask_as_images(mask.astype(np.uint8))
