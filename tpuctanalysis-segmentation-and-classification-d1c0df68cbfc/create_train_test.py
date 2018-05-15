import argparse
import numpy as np
import os
import shutil

from sklearn.model_selection import train_test_split
from tqdm import tqdm
from dicom_data_working import read_all_dicom_data
from dicom_saving import save_dicom_data
from utils import create_dirs
from config.feature_extraction_config import load_features_config as lf_opt
from config.data_splitting_config import train_test_options as tt_opt
from config.dicom_working_config import dicom_options as d_opt


def train_test_from_masked_dicoms(source_folder_path,
                                  test_split,
                                  target_folder_path,
                                  verbose=False):
    """
    Preforms stratified splitting all the data inside patient folders
    into train and test sets using a certain test ratio
    :param source_folder_path: Path to the directory contained patient folders
    :param test_split: Ratio of a test split
    :param target_folder_path: Path to the folder to save train and test data
    :param verbose: Whether to show progress report in a console
    """
    # Obtain information about class labels on slices - creating a registry
    data_registry = {}
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

            label_folder_path = os.path.join(survey_folder_path,
                                             lf_opt['label_folder_name'])
            __add_to_registry(label_folder_path, pfn, sfn, data_registry)

    if verbose:
        print('{} slices detected'.format(len(data_registry)))

    # Split all the slices set on train and test
    train_registry, test_registry = __split_registry(data_registry, test_split)

    # Create train and test dirs
    train_dir_path = os.path.join(target_folder_path, tt_opt['train_dir_name'])
    test_dir_path = os.path.join(target_folder_path, tt_opt['test_dir_name'])
    create_dirs([train_dir_path, test_dir_path])

    if verbose:
        print('Copying files to train and test directories...')

    # Save dicom data and copy label masks to the target folder according to partition
    for pfn in patient_folder_names:
        patient_folder_path = os.path.join(source_folder_path, pfn)
        train_patient_dir = os.path.join(train_dir_path, pfn)
        test_patient_dir = os.path.join(test_dir_path, pfn)
        create_dirs([train_patient_dir, test_patient_dir])

        survey_folder_names = sorted(os.listdir(patient_folder_path))
        for sfn in survey_folder_names:
            survey_folder_path = os.path.join(patient_folder_path, sfn)
            train_survey_dir = os.path.join(train_patient_dir, sfn)
            test_survey_dir = os.path.join(test_patient_dir, sfn)
            create_dirs([train_survey_dir, test_survey_dir])

            data_folder_names = sorted(os.listdir(survey_folder_path))

            # Check validity of data folder names
            if lf_opt['dicom_folder_name'] not in data_folder_names:
                raise FileNotFoundError('Patient {0}, survey {1} - {2} folder not found'
                                        .format(pfn, sfn, lf_opt['dicom_folder_name']))
            if lf_opt['label_folder_name'] not in data_folder_names:
                raise FileNotFoundError('Patient {0}, survey {1} - {2} folder not found'
                                        .format(pfn, sfn, lf_opt['label_folder_name']))

            # Create directories for new divided data
            train_dicom_dir = os.path.join(train_survey_dir, lf_opt['dicom_folder_name'])
            train_label_dir = os.path.join(train_survey_dir, lf_opt['label_folder_name'])
            create_dirs([train_dicom_dir, train_label_dir], remove_old=True)
            test_dicom_dir = os.path.join(test_survey_dir, lf_opt['dicom_folder_name'])
            test_label_dir = os.path.join(test_survey_dir, lf_opt['label_folder_name'])
            create_dirs([test_dicom_dir, test_label_dir], remove_old=True)

            # Read dicom data files and label file names
            dicom_folder_path = os.path.join(survey_folder_path,
                                             lf_opt['dicom_folder_name'])
            d_file_names = sorted(os.listdir(dicom_folder_path))
            dicom_file_names = []
            for fn in d_file_names:
                file_extension = fn.split('.')[-1]
                if file_extension in d_opt['extensions']:
                    dicom_file_names.append(fn)
            dicom_data_list = read_all_dicom_data(dicom_folder_path, dicom_file_names)

            label_folder_path = os.path.join(survey_folder_path,
                                             lf_opt['label_folder_name'])
            l_file_names = sorted(os.listdir(label_folder_path))
            label_file_names = []
            for fn in l_file_names:
                file_extension = fn.split('.')[-1]
                if file_extension in lf_opt['label_file_extensions']:
                    label_file_names.append(fn)

            assert len(dicom_data_list) == len(label_file_names)

            progress_bar = None
            if verbose:
                print('Copying data for patient {0}, survey {1}'.format(pfn, sfn))
                progress_bar = tqdm(total=len(dicom_data_list))

            # Saving dicom files and copying label files
            for i in range(len(dicom_data_list)):
                registry_key = pfn + '_' + sfn + '_' + str(i)
                dicom_file_name = tt_opt['dicom_file_pattern'].format(i)
                label_file_name = tt_opt['label_file_pattern'].format(i)

                if registry_key in train_registry:
                    save_dicom_data(dicom_data_list[i],
                                    os.path.join(train_dicom_dir, dicom_file_name))
                    shutil.copy2(os.path.join(label_folder_path, label_file_names[i]),
                                 os.path.join(train_label_dir, label_file_name))
                else:
                    save_dicom_data(dicom_data_list[i],
                                    os.path.join(test_dicom_dir, dicom_file_name))
                    shutil.copy2(os.path.join(label_folder_path, label_file_names[i]),
                                 os.path.join(test_label_dir, label_file_name))

                progress_bar.update(1)
            progress_bar.close()


def __add_to_registry(labels_folder_path, patient_id, survey_id, registry):
    """
    Extracts information about class labels of the slices using class labels binary masks.
    This function is updating registry dict inplace
    :param labels_folder_path: Path to the folder contained class label binary files
    :param patient_id: ID of a patient which class label masks are analysing
    :param survey_id: ID of a patient survey
    :param registry: Dictionary to write a new information about class labels
    """
    # Load label masks file names
    file_names = sorted(os.listdir(labels_folder_path))
    label_file_names = []
    for fn in file_names:
        file_extension = fn.split('.')[-1]
        if file_extension in lf_opt['label_file_extensions']:
            label_file_names.append(fn)

    # Read binary label files and add info to index
    key_base = str(patient_id) + '_' + str(survey_id) + '_{}'
    for i, lfn in enumerate(label_file_names):
        label_file_path = os.path.join(labels_folder_path, lfn)
        label_mask = np.load(label_file_path)
        uniques = np.unique(label_mask)

        key_ready = key_base.format(i)
        if uniques.shape[0] == 1:
            registry[key_ready] = 0
        else:
            registry[key_ready] = uniques[1]


def __split_registry(input_dict, test_split):
    """
    Performs train-test splitting with a certain train ratio
    :param input_dict: Dictionary contained inputs as keys and targets as values
    :param test_split: Ratio of a test split
    :return: Train and test dictionaries contained inputs as keys and targets as values
    """
    inp, tar = [], []
    for key in input_dict:
        inp.append(key)
        tar.append(input_dict[key])

    inp_train, inp_test, tar_train, tar_test = train_test_split(inp,
                                                                tar,
                                                                test_size=test_split,
                                                                shuffle=True,
                                                                stratify=tar)

    train_dict, test_dict = {}, {}
    for i in range(len(inp_train)):
        train_dict[inp_train[i]] = tar_train[i]
    for i in range(len(inp_test)):
        test_dict[inp_test[i]] = tar_test[i]

    return train_dict, test_dict


def main(source_folder_path,
         test_split,
         target_folder_path,
         verbose):
    """
    Main function
    """
    train_test_from_masked_dicoms(source_folder_path,
                                  float(test_split),
                                  target_folder_path,
                                  verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates train and test data sets '
                                                 'from the whole data')

    parser.add_argument(
        '-i',
        '--input_folder',
        help='Path to the folder contained patient folders'
    )

    parser.add_argument(
        '-ts',
        '--test_split',
        help='Share of test data from the whole amount of data. Default is 0.2',
        default='0.2'
    )

    parser.add_argument(
        '-o',
        '--output_folder',
        help='Path to the folder to save train and test data'
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
         args.test_split,
         args.output_folder,
         args.verbose)
