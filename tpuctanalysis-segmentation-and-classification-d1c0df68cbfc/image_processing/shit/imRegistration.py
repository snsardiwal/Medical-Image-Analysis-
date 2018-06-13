from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image
import numpy as np
from listFileNames import *
def command_iteration(method) :
    if (method.GetOptimizerIteration() == 0):
        print("\tLevel: {0}".format(method.GetCurrentLevel()))
        print("\tScales: {0}".format(method.GetOptimizerScales()))
    print("#{0}".format(method.GetOptimizerIteration()))
    print("\tMetric Value: {0:10.5f}".format( method.GetMetricValue()))
    print("\tLearningRate: {0:10.5f}".format(method.GetOptimizerLearningRate()))
    if (method.GetOptimizerConvergenceValue() != sys.float_info.max):
        print("\tConvergence Value: {0:.5e}".format(method.GetOptimizerConvergenceValue()))


def command_multiresolution_iteration(method):
    print("\tStop Condition: {0}".format(method.GetOptimizerStopConditionDescription()))
    print("============= Resolution Change =============")


def imageRegistration(im1,im2):
    
    LIST="/Users/sachin/Desktop/CT_Project/data1.tfm"

    #read images
    fixed = sitk.ReadImage(im1, sitk.sitkFloat32)
    #fixed=sitk.RGBToLuminanceImageFilter.New(fixed)
    moving = sitk.ReadImage(im2, sitk.sitkFloat32)
    #moving=sitk.RGBToLuminanceImageFilter(moving)

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
    R.SetMetricAsANTSNeighborhoodCorrelation(4)
    R.MetricUseFixedImageGradientFilterOff()
    R.MetricUseFixedImageGradientFilterOff()


    R.SetShrinkFactorsPerLevel([3,2,1])
    R.SetSmoothingSigmasPerLevel([2,1,1])

    #Optimizer Settings
    R.SetOptimizerScalesFromPhysicalShift()
    R.SetOptimizerAsGradientDescent(learningRate=1,
                                numberOfIterations=100,
                                estimateLearningRate=R.EachIteration)

    outTx.AddTransform( R.Execute(fixed, moving) )


    print("-------")
    print(outTx)
    print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
    print(" Iteration: {0}".format(R.GetOptimizerIteration()))
    print(" Metric value: {0}".format(R.GetMetricValue()))


    sitk.WriteTransform(outTx,  LIST)

    
    return outTx

def imageRegistrationFromFolder(folder_path_1,folder_path_2,NumberImagesToCompare=10):
    
    file_names1=listFileNames(folder_path_1)
    file_names2=listFileNames(folder_path_2)
    negRGB=[]
    im1AfterReg=[]
    im2AfterReg=[]
    
    for i in range(file_names1.shape[0]):
        image_path_1=os.path.join(folder_path_1,file_names1[i])
        count=-NumberImagesToCompare//2
        
        while(count<NumberImagesToCompare/2+1):
            ii=i+count
            if (ii>=0) and (ii < file_names2.shape[0]):
                image_path_2=os.path.join(folder_path_2,file_names2[ii])
                im1,im2,nda=imageRegistration(image_path_1,image_path_2)
                
                
                im1Gray=Image.fromarray(im1.astype('uint8')).convert('L')
                im2Gray=Image.fromarray(im2.astype('uint8')).convert('L')

                nda=Image.fromarray(nda)
                
                im1Gray.save("image1.png")
                im2Gray.save("image2.png")
                #im1befGray=Image.open(image_path_1).convert('L')
                #im2befGray=Image.open(image_path_2).convert('L')



                Lbef,negGrayBef=compareImages(image_path_1,image_path_2)
                Lafter,negGray=compareImages("image1.png","image2.png")
                print(negGrayBef.shape)
                negGray[negGray!=255]=0
                negGrayBef[negGrayBef!=255]=0
                negGrayBef=Image.fromarray(negGrayBef).convert('L')
                negGray=Image.fromarray(negGray).convert('L')

                folder_path_to_save1="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/boneMask/Patient6/bef"
                folder_path_to_save2="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/boneMask/Patient6/after"
                folder_path_to_save3="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/boneMask/Patient6/colormap"
                filename="%s_%s" % (file_names1[i],file_names2[ii])
                
                negGrayBef.save(os.path.join(folder_path_to_save1,filename))
                negGray.save(os.path.join(folder_path_to_save2,filename))
                nda.save(os.path.join(folder_path_to_save3,filename))

                #Saving the findings in log file
                result="%s %s %d %d" % (i,ii,Lbef,Lafter)
                with open('patient6Bone.log','a') as f:
                    f.write(result)
                    f.write('\n')

                im1AfterReg.append(im1)
                im2AfterReg.append(im2)
                negRGB.append(nda)

                #filename="%s_%s"%(i,ii) + ".png"
                
                #neg_image=scipy.misc.toimage(neg_image)
                #print(filename)
                #neg_image.save(os.path.join(folder_path_to_save,filename))
            count=count+1

    return im1AfterReg,im2AfterReg,neg_image

                           