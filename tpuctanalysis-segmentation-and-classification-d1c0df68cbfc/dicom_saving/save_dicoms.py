import dicom
import os
import sys

sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/dicom_data_working")

from PIL import Image
from config.dicom_working_config import dicom_options as d_opt
from feature_extraction import extract_glcm_from_image_array
from open_dicoms import extract_dicom_slices_from_folder
from tissue_masking import get_bone_mask
from convert_dicoms import normalize_slices_for_images
def save_slices_as_images(dicom_slices, folder_path_to_save):
    """
    Saves dicom slices pixel data as a set of images in the folder
    :param dicom_slices: ndarray of dicom slices pixel data
    :param folder_path_to_save: Path to the folder to save dicom images
    """
    for i in range(dicom_slices.shape[0]):
        ct_image = Image.fromarray(dicom_slices[i])
        ct_image_path = os.path.join(folder_path_to_save,
                                     d_opt['filename_pattern'].format(i))
        ct_image.save(ct_image_path)


def save_ct_images(images, folder_path_to_save):
    """
    Saves ready slice images in the folder
    :param images: List of PIL Image objects
    :param folder_path_to_save: Path to the folder to save
    """
    for i in range(len(images)):
        image_path = os.path.join(folder_path_to_save,
                                  d_opt['filename_pattern'].format(i))
        images[i].save(image_path)


def save_dicom_data(dicom_file_data, file_path_to_save, with_original_meta=True):
    """
    Saves dicom data as a dicom file
    :param dicom_file_data: Dicom data like pydicom.dataset.FileDataset
    :param file_path_to_save: Full path to the file to save as a dicom file
    :param with_original_meta: Whether to save new file with original metadata.
    If original file does not have metadata writes None
    """
    dicom.write_file(file_path_to_save,
                     dicom_file_data,
                     write_like_original=with_original_meta)

folder_path="/Users/sachin/Desktop/CT_Project/datasets/clinical_records_20180205_092007_186/186/CT/20130211"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/dicom_images/ct/20130211"

dicom_slices=extract_dicom_slices_from_folder(folder_path,0,0)
normalized_slices=normalize_slices_for_images(dicom_slices)
save_slices_as_images(normalized_slices,folder_path_to_save)
