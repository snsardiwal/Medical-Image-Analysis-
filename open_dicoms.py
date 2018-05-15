import dicom
import numpy as np
import os
import sys

#sys.path.insert(0, "/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc")

from config.dicom_working_config import dicom_options as d_opt

folder_path="/Users/sachin/Desktop/CT_Project/datasets/clinical_records_20180205_092007_186/186/CT/20130124"

def extract_dicom_slices_from_folder(folder_path,
                                     except_from_start=0,
                                     except_from_end=0):
    """
    Creates a dicom slices pixel data array in a certain radiology preset
    from a set of dicom-files stored in the folder
    :param folder_path: Path to the directory contained dicom-files
    :param except_from_start: A number of slices to except from the start
    :param except_from_end: A number of slices to except from the end
    :return: An array of dicom slices pixel data in a certain radiology preset
    """
    # Read dicom file names from the folder
    file_names = sorted(os.listdir(folder_path))
    dicom_file_names = []
    for fn in file_names:
        file_extension = fn.split('.')[-1]
        if file_extension in d_opt['extensions']:
            dicom_file_names.append(fn)

    # Load ordered dicom slices
    dicom_data_list = read_all_dicom_data(folder_path, dicom_file_names)
    dicom_slices = __load_all_slices(dicom_data_list)

    # Except slices if needed
    dicom_slices = __except_slices(dicom_slices, except_from_start, except_from_end)
    return dicom_slices


def read_all_dicom_data(dicom_folder_path, dicom_file_names):
    """
    Reads dicom data as a set of dicom-slices in a right order
    :param dicom_folder_path: Path to the directory contained dicom files
    :param dicom_file_names: List of dicom file names contained in the folder
    :return: List of dicom files presented as a set of dicom slices data
    """
    dicom_data_list = [dicom.read_file(os.path.join(dicom_folder_path, dfn))
                       for dfn in dicom_file_names]
    dicom_data_list.sort(key=lambda x: int(x.InstanceNumber))
    return dicom_data_list


def __load_all_slices(dicom_data_list):
    """
    Loads the pixel data from the list of dicom slices data
    :param dicom_data_list: List of dicom slices data
    :return: ndarray of dicom slices pixel data
    """
    dicom_slices = np.stack([data.pixel_array for data in dicom_data_list])
    return dicom_slices.astype(np.int16)


def __except_slices(dicom_slices, from_start, from_end):
    """
    Removes the certain number of slices from the set dicom slices pixel data
    :param dicom_slices: ndarray of dicom slices pixel data
    :param from_start: A number of slices to except from start
    :param from_end: A number of slices to except from end
    :return: reduced ndarray of dicom slices pixel data
    """
    assert from_start >= 0
    assert from_start < dicom_slices.shape[0]
    assert from_end >= 0
    assert from_end < dicom_slices.shape[0]
    assert from_start + from_end < dicom_slices.shape[0]

    start_index = from_start
    end_index = dicom_slices.shape[0] - from_end
    return dicom_slices[start_index: end_index, ...]


#def main():
 #   pass


#if __name__ == '__main__':
 #   main()

