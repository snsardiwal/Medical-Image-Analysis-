import numpy as np
import sys

from config.dicom_working_config import dicom_options as d_opt
from config.dicom_working_config import radiology_preset_options as rp_opt


def convert_slices_to_preset(dicom_slices, preset):
    """
    Converts the pixel data of dicom slices according to radiology preset
    and normalize
    :param dicom_slices: ndarray of original dicom slices pixel data
    :param preset: radiology preset to covert dicom pixel data
    :return: ndarray of dicom slices pixel data converted according to preset
    """
    presets = d_opt['radiology_preset']
    left_border = rp_opt['left_border_dicom']
    right_border = rp_opt['right_border_dicom']

    if preset == presets['soft']:
        left_level = rp_opt['soft_preset_dicom']['left']
        right_level = rp_opt['soft_preset_dicom']['right']
    elif preset == presets['lung']:
        left_level = rp_opt['lung_preset_dicom']['left']
        right_level = rp_opt['lung_preset_dicom']['right']
    elif preset == presets['pleural']:
        left_level = rp_opt['pleural_preset_dicom']['left']
        right_level = rp_opt['pleural_preset_dicom']['right']
    elif preset == presets['bone']:
        left_level = rp_opt['bone_preset_dicom']['left']
        right_level = rp_opt['bone_preset_dicom']['right']
    else:
        left_level = left_border
        right_level = right_border

    if left_level < left_border:
        left_level = left_border
    if right_level > right_border:
        right_level = right_border

    dicom_slices[dicom_slices < left_level] = left_level
    dicom_slices[dicom_slices > right_level] = right_level
    dicom_slices[dicom_slices < left_border] = 0
    dicom_slices[dicom_slices > right_border] = 0

    return normalize_slices_for_images(dicom_slices,
                                       min_value=left_level,
                                       max_value=right_level)


def normalize_slices_for_images(dicom_slices, min_value=None, max_value=None):
    """
    Makes a min-max normalization of dicom_slices values
    to convert them into the range [0; 255]
    :param dicom_slices: ndarray of dicom slices pixel data
    :param min_value: optional min value to normalize
    :param max_value: optional max value to normalize
    :return: ndarray of dicom slices pixel data normalized in [0; 255] range
    """
    # Obtain min and max values to normalize
    if min_value is None:
        min_value = np.min(dicom_slices)
    if max_value is None:
        max_value = np.max(dicom_slices)
        #print(max_value)
    # Normalization
    result_dicom_slices = ((dicom_slices - min_value) / (max_value - min_value)) * 255

    return result_dicom_slices.astype(np.uint8)

