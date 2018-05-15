"""
This file contains constants to load DICOM files
"""

dicom_options = {
    'extensions': ['dcm', 'dicom'],
    'radiology_preset': {
        'wide': 0,
        'soft': 1,
        'lung': 2,
        'pleural': 3,
        'bone': 4
    },
    'filename_pattern': '{:03d}.png'
}

radiology_preset_options = {
    'left_border_dicom': 0,
    'right_border_dicom': 3600,
    'soft_preset_dicom': {
        'left': 852,
        'right': 1277
    },
    'lung_preset_dicom': {
        'left': -164,
        'right': 712
    },
    'pleural_preset_dicom': {
        'left': -301,
        'right': 1449
    },
    'bone_preset_dicom': {
        'left': 524,
        'right': 2024
    }
}

radiology_tissue_options = {
    'min_dicom': 0,
    'max_dicom': 3600,
    'bone_dicom': {
        'left':1424,
        'right': 3600
    }
}
