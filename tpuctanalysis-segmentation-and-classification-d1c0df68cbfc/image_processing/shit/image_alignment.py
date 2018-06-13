from __future__ import print_function
import cv2
import numpy as np
from listFileNames import listFileNames
import os

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15
 
MATCH_NUMBER=10
def alignImages(im1, im2):
 
  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
   
  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(MAX_FEATURES)
  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
   
  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)
   
  # Sort matches by score
  matches.sort(key=lambda x: x.distance, reverse=False)
 
  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]
 
  # Draw top matches
  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  cv2.imwrite("matches.jpg", imMatches)
   
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
 
  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
   
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
 
  # Use homography
  height, width, channels = im1.shape
  im2Reg = cv2.warpPerspective(im2, h, (width, height))
   
  return im2Reg, h
 
def alignImagesInFolder(refFolderPath,folderPath,n):
  reflist=listFileNames(refFolderPath)
  list2=listFileNames(folderPath)

  folder_path_to_save="/Users/sachin/Desktop/CT_Project/stats/patient%s/wrapImages"%(n)
  folder_path_neg="/Users/sachin/Desktop/CT_Project/stats/patient%s/negImages"%(n)
  folder_path_negAlign="/Users/sachin/Desktop/CT_Project/stats/patient%s/negImagesAlign"%(n)
  
  
  os.mkdir("/Users/sachin/Desktop/CT_Project/stats/patient%s"%(n))
  os.mkdir(folder_path_to_save)
  os.mkdir(folder_path_neg)
  os.mkdir(folder_path_negAlign)

  for i in range(reflist.shape[0]):
    imRefPath=os.path.join(refFolderPath,reflist[i])
    imRef=cv2.imread(imRefPath,cv2.IMREAD_COLOR)
    count=-MATCH_NUMBER//2
    while(count<=MATCH_NUMBER):
      ii=i+count
      if((ii>=0) and (ii<list2.shape[0])):
        imPath=os.path.join(folderPath,list2[ii])
        im=cv2.imread(imPath,cv2.IMREAD_COLOR)
        imReg,h=alignImages(imRef,im)

        negImage=cv2.subtract(imRef,im)
        negImageAlign=cv2.subtract(imRef,imReg)

        filename="%s_%s" %(reflist[i],list2[ii])
        cv2.imwrite(os.path.join(folder_path_to_save,filename),imReg)
        cv2.imwrite(os.path.join(folder_path_neg,filename),negImage)
        cv2.imwrite(os.path.join(folder_path_negAlign,filename),negImageAlign)
      count=count+1
  
 
if __name__ == '__main__':
   
  # Read reference image
  #refFilename = "/Users/sachin/Desktop/CT_Project/paint_images/077.png"
  #print("Reading reference image : ", refFilename)
  #imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
 
  # Read image to be aligned
  #imFilename = "/Users/sachin/Desktop/CT_Project/paint_images/078.png"
  #print("Reading image to align : ", imFilename);  
  #im = cv2.imread(imFilename, cv2.IMREAD_COLOR)
   
  #print("Aligning images ...")
  # Registered image will be resotred in imReg. 
  # The estimated homography will be stored in h. 
  #imReg, h = alignImages(im, imReference)
   
  # Write aligned image to disk. 
  #outFilename = "/Users/sachin/Desktop/CT_Project/paint_images/aligned.jpg"
  #print("Saving aligned image : ", outFilename); 
  #cv2.imwrite(outFilename, imReg)
 
  # Print estimated homography
  #print("Estimated homography : \n",  h)
  refFolderPath="/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20121102"
  folderPath="/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20130301"
  alignImagesInFolder(refFolderPath,folderPath,6)