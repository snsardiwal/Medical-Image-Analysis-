

from segment_ct_slices import *



folder_path="/Users/sachin/Desktop/CT_Project/datasets/old/clinical_records_20180205_092007_186/186/CT/20130124"
target_dir="/Users/sachin/Desktop/CT_Project/images/boneMask/xyz"
radiology_preset='soft'
except_from_start=40
except_from_end=40

segment_lungs_from_dicoms(folder_path,
	radiology_preset,
	except_from_start,
	except_from_end,
	target_dir)