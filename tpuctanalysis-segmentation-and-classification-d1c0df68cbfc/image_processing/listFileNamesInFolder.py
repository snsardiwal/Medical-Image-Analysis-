import os
import numpy as np
from PIL import Image
import scipy.misc

def listFileNames(folderPath):
  fileNames=sorted(os.listdir(folderPath))
  dicomFileNames=[]
  
  for fn in fileNames:
    file_extension=fn.split('.')[-1]
    if file_extension=='png' or file_extension=='jpg':
      dicomFileNames.append(fn)
  dicomFileNames=np.array(dicomFileNames)
  return dicomFileNames


