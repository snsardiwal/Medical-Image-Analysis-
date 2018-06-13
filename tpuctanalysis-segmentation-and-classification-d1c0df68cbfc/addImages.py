import cv2
import numpy as np
from image_processing.listFileNamesInFolder import *
from PIL import Image



def add(file_path1,file_path2):
	file1=Image.open(file_path1)
	file2=Image.open(file_path2).convert('L')

	file1_array=np.uint8(np.array(file1))
	file2_array=np.uint8(np.array(file2))
	
	addition=cv2.add(file1_array,file2_array)
	return addition

def addFolder(folder_path1,folder_path2,tar_folder):
	filelist1=listFileNames(folder_path1)
	filelist2=listFileNames(folder_path2)

	sumImages=[]
	for i in range(filelist1.shape[0]):
		file_path1=os.path.join(folder_path1,filelist1[i])
		file_path2=os.path.join(folder_path2,filelist2[i])

		addition=add(file_path1,file_path2)
		addition=Image.fromarray(addition)
		addition.save(tar_folder+ "/%03d.png" % (i))

	


folder_path1="/Users/sachin/Desktop/CT_Project/images/lungMask/patient1/time2"
folder_path2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient1/time2"
tar_folder="/Users/sachin/Desktop/CT_Project/images/boneLungMask/patient1/time2"
#addFolder(folder_path1,folder_path2,tar_folder)

a=addFolder(folder_path1,folder_path2,tar_folder)
#print(a[175])
#a=Image.fromarray(a)
#a.save('add.png')
#print(a[200])
#print('\n')
#b=Image.open(folder_path2)
#b=np.array(b)
#print(b[175])
