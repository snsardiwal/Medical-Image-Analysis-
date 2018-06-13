from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image
import numpy as np
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/image_processing")
from listFileNamesInFolder import listFileNames
from returnRegisteredImage import *
from compareMask import *
import csv
def imageRegistration(im1,im2):
    
    #LIST="/Users/sachin/Desktop/CT_Project/data1.tfm"

    #read images
    fixed = sitk.ReadImage(im1, sitk.sitkFloat32)
    #fixed=sitk.RGBToLuminanceImageFilter.New(fixed)
    moving = sitk.ReadImage(im2, sitk.sitkFloat32)
    #moving=sitk.RGBToLuminanceImageFilter(moving)

    fixed_array=sitk.GetArrayFromImage(fixed)
    moving_array=sitk.GetArrayFromImage(moving)

    if np.amax(fixed_array)==0 or np.amax(moving_array)==0:
        return 0,0

    else:

        #Initial Alignment
        initialTx = sitk.CenteredTransformInitializer(fixed, moving, sitk.AffineTransform(fixed.GetDimension()))

        R = sitk.ImageRegistrationMethod()

        #Setup for Multiresolution framework
        R.SetShrinkFactorsPerLevel([3,2,1])
        R.SetSmoothingSigmasPerLevel([2,1,1])

        #Similarity Metric Settings
        R.SetMetricAsJointHistogramMutualInformation(20)
        R.MetricUseFixedImageGradientFilterOff()
        #R.MetricUseFixedImageGradientFilterOff()

        #Optimizer Settings
        R.SetOptimizerAsGradientDescent(learningRate=1.0,
                                numberOfIterations=100,
                                estimateLearningRate = R.EachIteration)
        R.SetOptimizerScalesFromPhysicalShift()

        #Optimize in-place
        R.SetInitialTransform(initialTx,inPlace=True)

        #Interpolator Settings
        R.SetInterpolator(sitk.sitkLinear)

        #Connect all of the observers so that we can perform plotting during registration
        R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )
        R.AddCommand( sitk.sitkMultiResolutionIterationEvent, lambda: command_multiresolution_iteration(R) )

        outTx = R.Execute(fixed, moving)


        print("-------")
        print(outTx)
        print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
        print(" Iteration: {0}".format(R.GetOptimizerIteration()))
        print(" Metric value: {0}".format(R.GetMetricValue()))
    
        #Tranformation settings 
        displacementField = sitk.Image(fixed.GetSize(), sitk.sitkVectorFloat64)
        displacementField.CopyInformation(fixed)
        displacementTx = sitk.DisplacementFieldTransform(displacementField)
        del displacementField
        displacementTx.SetSmoothingGaussianOnUpdate(varianceForUpdateField=0.0,
                                            varianceForTotalField=1.5)



        R.SetMovingInitialTransform(outTx)
        R.SetInitialTransform(displacementTx, inPlace=True)

        #Similarity Metric Settings
        R.SetMetricAsANTSNeighborhoodCorrelation(2)
        R.MetricUseFixedImageGradientFilterOff()
        R.MetricUseFixedImageGradientFilterOff()


        R.SetShrinkFactorsPerLevel([3,2,1])
        R.SetSmoothingSigmasPerLevel([2,1,1])

        #Optimizer Settings
        R.SetOptimizerScalesFromPhysicalShift()
        R.SetOptimizerAsGradientDescent(learningRate=1,
                                numberOfIterations=300,
                                estimateLearningRate=R.EachIteration)

        outTx.AddTransform( R.Execute(fixed, moving) )


        print("-------")
        print(outTx)
        print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
        print(" Iteration: {0}".format(R.GetOptimizerIteration()))
        print(" Metric value: {0}".format(R.GetMetricValue()))


        #sitk.WriteTransform(outTx,  LIST)

        cimg,im2=returnMovingImage(outTx,fixed,moving)
        return cimg,im2

def imageRegistrationFromFolder(folder_path1,folder_path2,NumberImagesToCompare=10):
    
    file_names1=listFileNames(folder_path1)
    file_names2=listFileNames(folder_path2)
    
    im2_array=[]
    for i in range(file_names1.shape[0]):
        image_path1=os.path.join(folder_path1,file_names1[i])
        count=-NumberImagesToCompare//2
        
        while(count<NumberImagesToCompare/2+1):
            ii=i+count
            if (ii>=0) and (ii < file_names2.shape[0]):
                
                image_path2=os.path.join(folder_path2,file_names2[ii])
                cimg,im2=imageRegistration(image_path1,image_path2)
                im2_array.append(im2)
            
            count=count+1

    return im2_array

def registerAndCompareImagesInFolder(folder_path1,folder_path2,file_to_write_large,file_to_write_small,folder_path_to_save,NumberOfImages=10):

    filenames1=listFileNames(folder_path1)
    filenames2=listFileNames(folder_path2)

    matchIndexAfterReg=np.empty(filenames1.shape[0])
    matchPixelCountAfterReg=np.empty(filenames1.shape[0])
    
    for index1 in range(filenames1.shape[0]):
        
        im1_path=os.path.join(folder_path1,filenames1[index1])
        im1=Image.open(im1_path).convert('L')
        im1_array=np.array(im1,dtype='uint8')
        count=-NumberOfImages//2
        
        if np.sum(im1_array)!=0:
            while(count<NumberOfImages//2+1):
            
                index2=index1+count
            
                if count==-NumberOfImages//2:
                    matchIndexAfterReg[index1]=index2
                    matchPixelCountAfterReg[index1]=10000000

                if(index2>=0 and index2<filenames2.shape[0]):
                
                    im2_path=os.path.join(folder_path2,filenames2[index2])
                    im2=Image.open(im2_path).convert('L')
                    im2_before_reg_array=np.array(im2)
                    cimg,im2_after_reg_array=imageRegistration(im1_path,im2_path)

                    if np.sum(im2_before_reg_array)!=0:

                        cimg=Image.fromarray(cimg)
                        s="/%d_%d" % (index1,index2)+'.png'
                        cimg.save(folder_path_to_save+s)
                        pixelCountBeforeReg,negImageBefReg=compareImages(im1_array,im2_before_reg_array)
                        pixelCountAfterReg,negImageAfterReg=compareImages(im1_array,im2_after_reg_array)

            
                        #string1="%03d %03d %d %d" % (index1,index2,pixelCountBeforeReg,pixelCountAfterReg)
                        string1="%03d,%03d,%d,%d" % (index1,index2,pixelCountBeforeReg,pixelCountAfterReg)
                        with open(file_to_write_large,'a') as f:
                            writer=csv.writer(f,delimiter=',')
                            enteries=string1.split(",")
                            writer.writerow(enteries)
                            #f.write(string1)
                            #f.write('\n')

                        if pixelCountAfterReg<matchPixelCountAfterReg[index1]:
                            matchIndexAfterReg[index1]=index2
                            matchPixelCountAfterReg[index1]=pixelCountAfterReg

            
                count=count+1

            im2_pathMatch=os.path.join(folder_path2,"%03d"%(matchIndexAfterReg[index1])+".png")
            im2_Match=Image.open(im2_pathMatch).convert('L')
            im2_arrayMatch=np.array(im2_Match,dtype='uint8')

            pixelCountBefRegMatch,negImageBefRegMatch=compareImages(im1_array,im2_arrayMatch)
            string2="%03d,%03d,%d,%d" % (index1,matchIndexAfterReg[index1],pixelCountBefRegMatch,matchPixelCountAfterReg[index1])
            with open(file_to_write_small,'a') as f:
                writer=csv.writer(f,delimiter=',')
                enteries=string2.split(",")
                writer.writerow(enteries)
                #f.write(string2)
                #f.write('\n')

    return matchIndexAfterReg,matchPixelCountAfterReg


                           