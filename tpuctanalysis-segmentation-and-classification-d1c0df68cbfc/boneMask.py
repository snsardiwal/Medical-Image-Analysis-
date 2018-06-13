
import numpy as np
from dicom_data_working import extract_dicom_slices_from_folder
from dicom_data_working import convert_slices_to_preset
from dicom_saving import save_slices_as_images
from dicom_data_working.tissue_masking import get_bone_mask
from config.dicom_working_config import dicom_options as d_opt





def segment_bones_from_dicoms(folder_path,
			 				  radiology_preset,
			 				  except_from_start,
			 				  except_from_end,
			 				  target_dir):
	
	
    dicom_slices=extract_dicom_slices_from_folder(folder_path,
    											  except_from_start=except_from_start,
    											  except_from_end=except_from_end)

    bone_mask=get_bone_mask(dicom_slices)

    preset_slices=convert_slices_to_preset(dicom_slices,
    										d_opt['radiology_preset'][radiology_preset])

    save_slices_as_images((bone_mask*preset_slices).astype('uint8'),target_dir)


folder_path="/Users/sachin/Desktop/CT_Project/datasets/patient4/time2"
radiology_preset='bone'
target_dir="/Users/sachin/Desktop/CT_Project/images/boneMask/patient4/time2"

segment_bones_from_dicoms(folder_path,'bone',30,20,target_dir)

