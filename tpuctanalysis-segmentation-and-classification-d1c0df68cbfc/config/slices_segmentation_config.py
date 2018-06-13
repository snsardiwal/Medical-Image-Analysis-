"""
This file contains constants for segmentation of CT-slices
"""
type_of_segments = {
    'lungs': 0,
    'body': 1
}

lungs_segmentation = {
    'erosion_filter_size': 3,
    'dilation_filter_size': 9
}

body_segmentation = {
    'erosion_filter_size': 15,
    'dilation_filter_size': 7
}
