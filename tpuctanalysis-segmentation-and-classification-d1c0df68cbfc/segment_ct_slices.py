import argparse
import numpy as np

from dicom_data_working import extract_dicom_slices_from_folder
from dicom_data_working import convert_slices_to_preset
from dicom_saving import save_slices_as_images
from slices_segmentation import get_lungs_masks_for_slices
from config.dicom_working_config import dicom_options as d_opt


def segment_lungs_from_dicoms(folder_path,
                              radiology_preset,
                              except_from_start,
                              except_from_end,
                              target_dir):
    """
    Performs the lungs segmentation on the CT-slices loaded from dicom files
    :param folder_path: Path to the folder contained dicom files
    :param radiology_preset: A mode for dicom-images representation
    :param except_from_start: A number of slices to except from the start
    :param except_from_end: A number of slices to except from the end
    :param target_dir: Path to the folder to save dicom images
    """
    # Load dicom slices pixel data from the dicom files
    dicom_slices = extract_dicom_slices_from_folder(folder_path,
                                                    except_from_start=except_from_start,
                                                    except_from_end=except_from_end)
    # Obtain the mask for lung segments
    lungs_mask = get_lungs_masks_for_slices(dicom_slices)

    # Obtain converted to certain radiology preset slices
    preset_slices = convert_slices_to_preset(dicom_slices,
                                             d_opt['radiology_preset'][radiology_preset])

    # Save masks as images
    save_slices_as_images((preset_slices * lungs_mask).astype(np.uint8), target_dir)


def main(folder_path,
         radiology_preset,
         except_from_start,
         except_from_end,
         target_dir):
    """
    Main function
    """
    segment_lungs_from_dicoms(folder_path,
                              radiology_preset,
                              int(except_from_start),
                              int(except_from_end),
                              target_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads slices from dicom files '
                                                 'and perform a CT slices segmentation')

    parser.add_argument(
        '-i',
        '--dicoms_folder',
        help='Path to the folder contained dicom files'
    )

    parser.add_argument(
        '-r',
        '--radiology_preset',
        help='Mode of dicom images representation. One from the following:'
             'wide, soft, lung, pleural, bone. Default is wide.',
        default='wide'
    )

    parser.add_argument(
        '-s',
        '--start_exc',
        help='A number of dicom slices to except from the start of a slices set.'
             'Default is 0',
        default='0'
    )

    parser.add_argument(
        '-e',
        '--end_exc',
        help='A number of dicom slices to except from the end of a slices set.'
             'Default is 0',
        default='0'
    )

    parser.add_argument(
        '-o',
        '--output_folder',
        help='Path to the folder to save dicom images'
    )

    args = parser.parse_args()

    main(args.dicoms_folder,
         args.radiology_preset,
         args.start_exc,
         args.end_exc,
         args.output_folder)
