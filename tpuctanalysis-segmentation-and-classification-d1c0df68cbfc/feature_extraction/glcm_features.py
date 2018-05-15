import numpy as np
import math

from PIL import Image
from skimage.feature import greycomatrix
from config.feature_extraction_config import glcm_feature_options as gf_opt


def extract_glcm_from_image_array(patient_id,
                                  survey_id,
                                  slice_idx,
                                  image_array,
                                  label_mask,
                                  window_size,
                                  levels_count):
    """
    Extracts GLCM features form the greyscale ct image (Numpy array)
    using information about patient and class labels for the ct image
    :param patient_id: ID of the patient
    :param survey_id: ID of the patient survey
    :param slice_idx: Index of the CT slice
    :param image_array: Numpy array of the ct image of shape (height, width)
    :param label_mask: Numpy array presented class labels
    for the ct image of shape (height, width)
    :param window_size: Hyper parameter of the GLCM algorithm -
    size of the window to extract image intensities
    :param levels_count: Hyper parameter of the GLCM algorithm -
    number of the intensities to quantify the image
    :return: Features array of shape (informative image pixels count, features count)
    Features:
    - Target class label
    - Patient id
    - Survey id
    - CT slice index
    - X coordinate of the pixel
    - Y coordinate of the pixel
    - N GLCM features (N depends on algorithm hyper parameters)
    """
    assert image_array.dtype == np.uint8
    assert label_mask.dtype == np.uint8
    assert image_array.shape == label_mask.shape

    # Change window size if its value is not even
    if window_size % 2 == 0:
        window_size = window_size - 1

    # Quantification of the image
    img = Image.fromarray(image_array)
    quant_img = img.quantize(colors=levels_count)
    quant_image_array = np.array(quant_img)

    # Perform GLCM for image
    distances = gf_opt['distances']
    angles = gf_opt['angles']
    features = []
    height, width = quant_image_array.shape
    offset = math.floor(window_size / 2)

    # TODO: reduce features vector, because matrix is symmetric
    for y in range(height):
        for x in range(width):
            window = __get_window_data(quant_image_array, offset, x, y)
            if __check_array_informative(window):
                glcm_features_array = greycomatrix(window,
                                                   distances,
                                                   angles,
                                                   levels=levels_count)
                features.append(__get_features_record(label_mask[y, x],
                                                      patient_id,
                                                      survey_id,
                                                      slice_idx,
                                                      x,
                                                      y,
                                                      glcm_features_array))

    return np.array(features, dtype=np.int64)


def __get_window_data(array, offset, x, y):
    """
    Creates a fragment of the array by offset from the certain item
    (center of a fragment)
    :param array: Numpy array of shape (height, width)
    :param offset: Distance to offset from the certain point along x and y axes
    :param x: X coordinate of the item (center of a fragment)
    :param y: Y coordinate of the item (center of a fragment)
    :return: Numpy array of the input array of shape (2 * offset + 1, 2 * offset + 1)
    """
    left_offset = max(0, x - offset)
    right_offset = min(array.shape[1] - 1, x + offset)
    up_offset = max(0, y - offset)
    down_offset = min(array.shape[0] - 1, y + offset)
    return array[up_offset: down_offset + 1, left_offset: right_offset + 1]


def __check_array_informative(array):
    """
    Checks whether the array has more than one unique value
    :param array: Numpy array of any shape
    :return: True if input array has more than one unique value,
    false otherwise
    """
    return np.unique(array).shape[0] != 1


def __get_features_record(class_label,
                          patient_id,
                          survey_id,
                          slice_idx,
                          x,
                          y,
                          features_array):
    """
    Creates a record of features for object-features matrix
    :param class_label: Label number for class definition
    :param patient_id: ID of the patient
    :param survey_id: ID of the patient survey
    :param slice_idx: Index of the CT slice
    :param x: X coordinate of a pixel on the slice
    :param y: Y coordinate of a pixel on the slice
    :param features_array: Numpy array of GLCM features of any shape
    :return: Features record as a numpy array of shape (features number,)
    """
    primary_data = np.zeros((6, ))
    primary_data[0] = class_label
    primary_data[1] = patient_id
    primary_data[2] = survey_id
    primary_data[3] = slice_idx
    primary_data[4] = x
    primary_data[5] = y

    return np.hstack((primary_data, features_array.ravel()))
