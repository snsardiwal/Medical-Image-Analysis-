import argparse
import numpy as np
import os
import pandas as pd

from tqdm import tqdm
from dicom_data_working import extract_dicom_slices_from_folder
from slices_segmentation import get_lungs_masks_for_slices
from dicom_data_working import convert_slices_to_preset
from feature_extraction import extract_glcm_from_image_array
from config.dicom_working_config import dicom_options as d_opt
from config.feature_extraction_config import load_features_config as lf_opt
from config.feature_extraction_config import save_features_config as sf_opt
from config.feature_extraction_config import glcm_feature_options as gf_opt


def extract_from_patients_folder(source_folder_path,
                                 window_size,
                                 levels_count,
                                 folder_path_to_save,
                                 verbose=False):
    """
    Extracts GLCM features from all the patients data contained in the folder
    and save them in one CSV file
    :param source_folder_path: Path to the folder contained folders with patients data.
    Each folder with patient data must be named with patient id.
    Each patient folder should contain folders with survey data (folder name - survey id).
    Each survey folder should contain two folders, which names defined in the config file.
    Dicom-data folder should contain dicom files.
    Label-masks folder should contain binary class label masks for each dicom-file.
    :param window_size: Hyper parameter of GLCM algorithm
    :param levels_count: Hyper parameter of GLCM algorithm
    :param folder_path_to_save: Path to the folder to save features in a CSV file
    :param verbose: Whether to show progress report in the console
    """
    file_path_to_save = os.path.join(folder_path_to_save, sf_opt['features_file_name'])
    slice_sampling = int(sf_opt['slice_sampling_to_save'])

    features_size = 6 + (levels_count * levels_count *
                         len(gf_opt['distances']) * len(gf_opt['angles']))
    features_data = np.zeros((1, features_size))
    slices_processed = 0

    patient_folder_names = sorted(os.listdir(source_folder_path))
    for pfn in patient_folder_names:
        patient_folder_path = os.path.join(source_folder_path, pfn)
        survey_folder_names = sorted(os.listdir(patient_folder_path))
        for sfn in survey_folder_names:
            survey_folder_path = os.path.join(patient_folder_path, sfn)
            data_folder_names = sorted(os.listdir(survey_folder_path))

            # Check validity of data folder names
            if lf_opt['dicom_folder_name'] not in data_folder_names:
                raise FileNotFoundError('Patient {0}, survey {1} - {2} folder not found'
                                        .format(pfn, sfn, lf_opt['dicom_folder_name']))
            if lf_opt['label_folder_name'] not in data_folder_names:
                raise FileNotFoundError('Patient {0}, survey {1} - {2} folder not found'
                                        .format(pfn, sfn, lf_opt['label_folder_name']))

            # Obtain preset ct slice images contained only lungs
            dicom_folder_path = os.path.join(survey_folder_path,
                                             lf_opt['dicom_folder_name'])
            masked_image_arrays = __get_ct_images_for_lungs(dicom_folder_path)

            # Obtain label masks for classes on ct slice images
            label_folder_path = os.path.join(survey_folder_path,
                                             lf_opt['label_folder_name'])
            label_masks = __get_label_masks_from_folder(label_folder_path)

            # Obtain GLCM features
            patient_id = int(pfn)
            survey_id = int(sfn)
            progress_bar = None
            if verbose:
                print('Extract features for patient {0}, survey {1}'
                      .format(patient_id, survey_id))
                progress_bar = tqdm(total=masked_image_arrays.shape[0])

            for i in range(masked_image_arrays.shape[0]):
                features = extract_glcm_from_image_array(patient_id,
                                                         survey_id,
                                                         i,
                                                         masked_image_arrays[i],
                                                         label_masks[i],
                                                         window_size,
                                                         levels_count)
                features_data = np.vstack((features_data, features))

                # Count processed slices and save features after each 10th slice
                slices_processed = slices_processed + 1
                if slices_processed % slice_sampling == 0:
                    __append_to_csv(features_data, file_path_to_save)
                    features_data = np.zeros((1, features_size))

                if verbose:
                    progress_bar.update(1)
            progress_bar.close()

    # Append the rest of slices to csv file
    __append_to_csv(features_data, file_path_to_save)


def __get_ct_images_for_lungs(dicom_folder_path):
    """
    Extracts dicom data from the dicom files contained in a folder,
    segment lungs on the dicom data slices,
    convert slices to 'lung' radiology preset
    and returns lung-masked images
    :param dicom_folder_path: Path to the folder contained dicom files
    :return: Numpy array of lung-masked ct slices of shape (num slices, height, width)
    """
    dicom_slices = extract_dicom_slices_from_folder(dicom_folder_path)
    lung_masks = get_lungs_masks_for_slices(dicom_slices)
    preset_slices = convert_slices_to_preset(dicom_slices,
                                             d_opt['radiology_preset']['lung'])
    return (preset_slices * lung_masks).astype(np.uint8)


def __get_label_masks_from_folder(labels_folder_path):
    """
    Loads class label masks from the NPY files contained in the folder
    :param labels_folder_path: Path to the folder contained NPY label mask files
    :return: Numpy array of class labels for slices of shape (num slices, height, width)
    """
    # Load label masks file names
    file_names = sorted(os.listdir(labels_folder_path))
    label_file_names = []
    for fn in file_names:
        file_extension = fn.split('.')[-1]
        if file_extension in lf_opt['label_file_extensions']:
            label_file_names.append(fn)

    label_masks = []
    for lfn in label_file_names:
        label_file_path = os.path.join(labels_folder_path, lfn)
        label_masks.append(np.load(label_file_path))

    return np.array(label_masks, dtype=np.uint8)


def __append_to_csv(array_data, file_path):
    """
    Saves data from squared numpy array of integer values into a scv file.
    The new data is appended to existing data in the csv file.
    The function remove the first line from the input array if is is consisted of zeros.
    :param array_data: Squared numpy array of integer values
    :param file_path: Path to the csv file to save data
    """
    if len(array_data.shape) != 2:
        return

    if np.sum(array_data, axis=1)[0] == 0:
        array_data = np.delete(array_data, 0, axis=0)
    if array_data.shape[0] == 0:
        return

    array_data = array_data.astype(np.int64)
    df = pd.DataFrame(array_data)
    df.to_csv(file_path, index=False, header=False, mode='a')


def main(source_folder_path,
         window_size,
         levels_count,
         folder_path_to_save,
         verbose):
    """
    Main function
    """
    extract_from_patients_folder(source_folder_path,
                                 int(window_size),
                                 int(levels_count),
                                 folder_path_to_save,
                                 verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts GLCM features from the folder '
                                                 'contained folders with patients data')

    parser.add_argument(
        '-i',
        '--input_folder',
        help='Path to the folder contained patient folders'
    )

    parser.add_argument(
        '-w',
        '--window_size',
        help='Size of window to compute co-occurrence matrix. Default is 21',
        default='21'
    )

    parser.add_argument(
        '-l',
        '--levels_count',
        help='Number of quantification levels for ct image. Default is 3',
        default='4'
    )

    parser.add_argument(
        '-o',
        '--output_folder',
        help='Path to the folder to save CSV features file'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Whether to show progress report in the console. Default is False',
        default=False
    )

    args = parser.parse_args()

    main(args.input_folder,
         args.window_size,
         args.levels_count,
         args.output_folder,
         args.verbose)
