import sys
import os
import numpy as np

sys.path.insert(0, "/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/dicom_data_working")
sys.path.insert(0, "/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")

from open_dicoms import extract_dicom_slices_from_folder
from segment_lungs import get_lungs_masks_for_slices
from dicom_saving.save_dicoms import save_slices_as_images
from convert_dicoms import normalize_slices_for_images






folder_path="/Users/sachin/Desktop/CT_Project/datasets/new/clinical_records_20180410_062348_400/400/CT/20150410"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/lungmask/patient6_2"

dicom_slices=extract_dicom_slices_from_folder(folder_path,40,0)
lungMask1=get_lungs_masks_for_slices(dicom_slices)
normalized_slices=normalize_slices_for_images(lungMask1)
save_slices_as_images(normalized_slices,folder_path_to_save)
