import numpy as np

from sklearn.cluster import KMeans
from skimage import morphology
from skimage import measure
import sys
sys.path.insert(0, "/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
from config.slices_segmentation_config import body_segmentation as bs_conf


from dicom_data_working import extract_dicom_slices_from_folder
from dicom_saving import save_slices_as_images

def get_body_masks_for_slices(dicom_slices_array):
    """
    Performs the slices segmentation and returns a body mask for all slices
    :param dicom_slices_array: ndarray of original dicom slices pixel data
    :return: ndarray of dicom slices pixel data where values are equal to 1 or 0:
     1 is the pixel belonging to body, 0 is the pixel belonging to other structures
    """
    segmented_slices = []
    for s in dicom_slices_array:
        segmented_slices.append(get_body_mask_for_slice(s))

    return np.stack(segmented_slices)


def get_body_mask_for_slice(slice_array):
    """
    Performs the slices segmentation and returns a body mask
    :param slice_array: ndarray of a dicom slice data
    :return: ndarray of dicom slice data where values are equal to 1 or 0:
     1 is the pixel belonging to body, 0 is the pixel belonging to other structures
    """
    rows_num = slice_array.shape[0]
    cols_num = slice_array.shape[1]

    # Global image normalization
    global_mean = np.mean(slice_array)
    global_std = np.std(slice_array)
    norm_slice = slice_array - global_mean
    norm_slice = norm_slice / global_std

    # Find the mean value for the middle area of the slice
    middle_slice = norm_slice[int(cols_num / 5): int(cols_num / 5 * 4),
                              int(rows_num / 5): int(rows_num / 5 * 4)]
    middle_mean = np.mean(middle_slice)

    # Smoothing the intensity peaks by middle mean value
    norm_slice_min = np.min(norm_slice)
    norm_slice_max = np.max(norm_slice)
    norm_slice[norm_slice == norm_slice_min] = middle_mean
    norm_slice[norm_slice == norm_slice_max] = middle_mean

    # Use k-means to separate tissue background and air foreground of the middle
    kmeans = KMeans(n_clusters=2).\
        fit(np.reshape(middle_slice, [np.prod(middle_slice.shape), 1]))
    cluster_centers = sorted(kmeans.cluster_centers_.flatten())

    # Thresholding of the slice
    intencity_threshold = np.mean(cluster_centers)
    thresholded_slice = np.where(norm_slice > intencity_threshold, 1.0, 0.0)

    # Make erosion and dilation to smooth noises
    ef_size = bs_conf['erosion_filter_size']
    df_size = bs_conf['dilation_filter_size']
    eroded_slice = morphology.erosion(thresholded_slice, np.ones([ef_size, ef_size]))
    dilated_slice = morphology.dilation(eroded_slice, np.ones([df_size, df_size]))

    # Find regions which are fit to the estimated position of lungs
    labels = measure.label(dilated_slice)
    regions = measure.regionprops(labels)
    fit_labels = []
    for prop in regions:
        bbox = prop.bbox
        if (bbox[2] - bbox[0] >= rows_num / 3) and \
                (bbox[3] - bbox[1] >= cols_num / 4 * 3):
            fit_labels.append(prop.label)

    # Creating lungs mask
    body_mask = np.ndarray([rows_num, cols_num], dtype=np.uint8)
    body_mask[:] = 0
    for lb in fit_labels:
        body_mask = body_mask + np.where(labels == lb, 1, 0)
    body_mask = morphology.dilation(body_mask, np.ones([df_size, df_size]))

    return body_mask


#def main():
 #   pass


#if __name__ == '__main__':
 #   main()
folder_path="/Users/sachin/Desktop/CT_Project/datasets/patient9/time2"
target_dir="/Users/sachin/Desktop/CT_Project/images/bodyMask/patient9/time2"
dicom_slices=extract_dicom_slices_from_folder(folder_path,30,20)
body_mask=get_body_masks_for_slices(dicom_slices)
save_slices_as_images(body_mask.astype(np.uint8),target_dir)