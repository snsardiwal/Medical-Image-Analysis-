from image_processing.median_filter import *
import argparse


def main(folder_path,target_folder):

	"""
	Main Function
	"""
	applyMedianFilterFolder(folder_path,target_folder)


"""
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Load images from bone Mask'
												'and apply median filter')

	parser.add_argument(
		'-i',
		'--dicoms_folder',
		help='path to the folder contained dicom files')

	parser.add_argument(
		'-o',
		'--target_folder',
		help='path to the folder to save filtered images')

	args=parser.parse_args()

	main(args.dicoms_folder,args.target_folder)
"""
folder_path="/Users/sachin/Desktop/CT_Project/images/boneMask/patient4/time2"
target_folder="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient4/time2"
main(folder_path,target_folder)