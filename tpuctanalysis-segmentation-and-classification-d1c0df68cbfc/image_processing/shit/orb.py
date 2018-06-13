from __future__ import print_function
import cv2
import numpy as np
from listFileNames import listFileNames,negative,compare_images
import os
from PIL import Image
import scipy.misc
MAX_FEATURES = 1000
GOOD_MATCH_PERCENT = 0.5
 
MATCH_NUMBER=10
def alignImages(im1, im2):
 
  # Convert images to grayscale
 
  im1Gray = im1
  im2Gray = im2
   
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
  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
   
  return im1Reg, h
 
def alignImagesInFolder(refFolderPath,folderPath,n):
  reflist=listFileNames(refFolderPath)
  list2=listFileNames(folderPath)

  folder_path_to_save="/Users/sachin/Desktop/CT_Project/stats/patient%s/wrapImages"%(n)
  
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

        negImage=imRef-im
        negImageAlign=imRef-imReg

        filename="%s_%s" %(reflist[i],list2[ii])
        cv2.imwrite(os.path.join(folder_path_to_save,filename),imReg)
        cv2.imwrite(os.path.join(folder_path_neg,filename),negImage)
        cv2.imwrite(os.path.join(folder_path_negAlign,filename),negImageAlign)
      count=count+1
  
 
if __name__ == '__main__':
   


  # Read reference image
  refFilename = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient4/20100927/054.png"
  print("Reading reference image : ", refFilename)
  imReference = cv2.imread(refFilename)
  im1Gray = cv2.cvtColor(imReference, cv2.COLOR_BGR2GRAY)
 
  #Read image to be aligned
  imFilename = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient4/20110222/060.png"
  print("Reading image to align : ", imFilename);  
  im = cv2.imread(imFilename)
  im2Gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
  print("Aligning images ...")
  # Registered image will be resotred in imReg. 
  # The estimated homography will be stored in h. 
  imReg, h = alignImages(im, imReference)
  #cv2.imshow('image',im)
  #cv2.waitkey(0)
  # Write aligned image to disk. 
  outFilename = "aligned.jpg"
  print("Saving aligned image : ", outFilename); 
  cv2.imwrite(outFilename, imReg)


  neg,count=compare_images(refFilename,outFilename)
  neg=scipy.misc.toimage(neg)
  neg.save("negative_after.jpg")

  neg1,count1=compare_images(refFilename,imFilename)
  neg1=scipy.misc.toimage(neg1)
  neg1.save("negative_before.jpg")

  print("Dissimilarity between images before alignment:")
  print(count1)
  print("Dissimilarity between images after alignment:")
  print(count)
  