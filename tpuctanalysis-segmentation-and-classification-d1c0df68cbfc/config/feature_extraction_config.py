"""
This file contains constants for feature extraction
"""
import numpy as np

load_features_config = {
    'dicom_folder_name': 'dicom-data',
    'label_folder_name': 'label-masks',
    'label_file_extensions': [
        'npy'
    ]
}

save_features_config = {
    'features_file_name': 'features.csv',
    'slice_sampling_to_save': 10
}

glcm_feature_options = {
    'distances': [
        1
    ],
    'angles': [
        0,
        np.pi/4,
        np.pi/2,
        3*np.pi/4
    ]
}
