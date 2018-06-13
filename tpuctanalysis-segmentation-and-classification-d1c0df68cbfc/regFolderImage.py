
import os
import sys
import argparse
from PIL import Image
import numpy as np
from image_processing.compareMask import *
from image_processing.registration_displacement import *
from dicom_saving.save_dicoms import *


def main(folder_path1,
		folder_path2,
		file_path1,
		file_path2,
		folder_path_to_save,
		NumberOfImages=10):
	"""
	Main Function
	"""

	matchIndex,pixelDiff=registerAndCompareImagesInFolder(folder_path1,
														  folder_path2,
														  file_path1,
														  file_path2,
														  folder_path_to_save,
														  NumberOfImages=10)

	return matchIndex,pixelDiff
"""
if __name__ == '__main__':

	parser=argparse.ArgumentParser(description='Apply registration techniques to images'
												'and get aligned images')

	parser.add_argument(
		'-i1',
		'--input1',
		help='Path to the first folder')

	parser.add_argument(
		'-i2',
		'--input2',
		help='Path to the second folder')

	parser.add_argument(
		'-p1',
		'--path1',
		help='Path to the larger file')
	
	parser.add_argument(
		'-p2',
		'--path2',
		help='Path to the smaller file')
	
	parser.add_argument(
		'-n',
		'--number',
		help='Number of images in second' 
			 'folder which has to be compared'
			 'with images in first folder')

	args = parser.parse_args()

	matchIndex,pixeldiff=main(args.input1,
		 						   args.input2,
		 						   args.path1,
		 						   args.path2,
		 						   args.number)
"""
folder_path1="/Users/sachin/Desktop/CT_Project/images/bodyMask/patient2/time1"
folder_path2="/Users/sachin/Desktop/CT_Project/images/bodyMask/patient2/time2"
file_path1="/Users/sachin/Desktop/CT_Project/registration_data/patient2/body/dataL.csv"
file_path2="/Users/sachin/Desktop/CT_Project/registration_data/patient2/body/dataS.csv"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/bodyMask/patient2/colormap"
NumberOfImages=10
main(folder_path1,folder_path2,file_path1,file_path2,folder_path_to_save,NumberOfImages)
