import argparse

from dicom_data_working import extract_dicom_slices_from_folder
from dicom_data_working import convert_slices_to_preset
from dicom_data_working.tissue_masking import get_bone_mask
from slices_segmentation import get_lungs_masks_for_slices
from dicom_saving import save_slices_as_images
from dicom_saving import save_ct_images
from highlighting import highlight_mask_on_preset_slices
from config.dicom_working_config import dicom_options as d_opt


def read_dicoms_to_images(folder_path,
                          radiology_preset,
                          target_dir,
                          except_from_start,
                          except_from_end,
                          highlight_lungs,
                          highlight_bones):
    """
    Read dicom slices pixel data and saves it to the folder as dicom images
    :param folder_path: Path to the folder contained dicom files
    :param radiology_preset: A mode for dicom-images representation
    :param target_dir: Path to the folder to save dicom images
    :param except_from_start: A number of slices to except from the start
    :param except_from_end: A number of slices to except from the end
    :param highlight_lungs: Whether to highlight lung areas on the slice images
    :param highlight_bones: Whether to highlight bone areas on the slice images
    """
    dicom_slices = extract_dicom_slices_from_folder(folder_path,
                                                    except_from_start=except_from_start,
                                                    except_from_end=except_from_end)

    highlighting_masks = []
    if highlight_lungs:
        highlighting_masks.append(get_lungs_masks_for_slices(dicom_slices))
    if highlight_bones:
        highlighting_masks.append(get_bone_mask(dicom_slices))

    preset_slices = convert_slices_to_preset(dicom_slices,
                                             d_opt['radiology_preset'][radiology_preset])

    if len(highlighting_masks) == 0:
        save_slices_as_images(preset_slices, target_dir)
    else:
        highlighted_slices = highlight_mask_on_preset_slices(preset_slices, highlighting_masks)
        save_ct_images(highlighted_slices, target_dir)


def main(folder_path,
         radiology_preset,
         target_dir,
         except_from_start,
         except_from_end,
         highlight_lungs,
         highlight_bones):
    """
    Main function
    """
    if radiology_preset not in d_opt['radiology_preset']:
        print('The \'{}\' radiology preset is not a valid name'
              .format(radiology_preset))
        return

    read_dicoms_to_images(folder_path,
                          radiology_preset,
                          target_dir,
                          int(except_from_start),
                          int(except_from_end),
                          highlight_lungs,
                          highlight_bones)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads and saves '
                                                 'dicom slices pixel data')

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

    parser.add_argument(
        '-h_l',
        '--highlight_lungs',
        action='store_true',
        help='Highlight lung areas on the slice images',
        default=False
    )

    parser.add_argument(
        '-h_b',
        '--highlight_bones',
        action='store_true',
        help='Highlight bone areas on the slice images',
        default=False
    )

    args = parser.parse_args()

    main(args.dicoms_folder,
         args.radiology_preset,
         args.output_folder,
         args.start_exc,
         args.end_exc,
         args.highlight_lungs,
         args.highlight_bones)
