

from dicom_data_working import extract_dicom_slices_from_folder,convert_slices_to_preset
from dicom_saving import save_slices_as_images


folder_path = "/Users/sachin/Desktop/CT_Project/datasets/patient2/time1"
folder_path_to_save = "/Users/sachin/Desktop/CT_Project/images/dicomImages/patient2/time1/aftNorm"

dicom_slices = extract_dicom_slices_from_folder(folder_path,30,20)
preset_slices=convert_slices_to_preset(dicom_slices,2)
save_slices_as_images(preset_slices,folder_path_to_save)