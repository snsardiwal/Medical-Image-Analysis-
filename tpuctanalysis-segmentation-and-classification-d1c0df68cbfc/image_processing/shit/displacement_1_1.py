from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt 

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


def displacement(im1,im2):
    
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
    R.SetMetricAsJointHistogramMutualInformation(30)
    R.MetricUseFixedImageGradientFilterOff()
    #R.MetricUseFixedImageGradientFilterOff()

    #Optimizer Settings
    R.SetOptimizerAsGradientDescent(learningRate=2.0,
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


    sitk.WriteTransform(outTx,  LIST)

    if ( not "SITK_NOSHOW" in os.environ ):

    #sitk.Show(displacementTx.GetDisplacementField(), "Displacement Field")

        resampler = sitk.ResampleImageFilter()
        resampler.SetReferenceImage(fixed);
        resampler.SetInterpolator(sitk.sitkLinear)
        resampler.SetDefaultPixelValue(100)
        resampler.SetTransform(outTx)

        out = resampler.Execute(moving)
        simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
        simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
        cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)
        nda = sitk.GetArrayViewFromImage(cimg)
        nda = Image.fromarray(nda)
    return nda

def ImageRegistrationFromFolder(folder_path_1,folder_path_2,folder_path_to_save,
                                NumberImagesToCompare=10):
    
    file_names1=listFileNames(folder_path_1)
    file_names2=listFileNames(folder_path_2)
    neg_image=[]
    for i in range(file_names1.shape[0]):
        image_path_1=os.path.join(folder_path_1,file_names1[i])
        count=-NumberImagesToCompare/2
        while(count<NumberImagesToCompare/2+1):
            ii=i+count
            if (ii>=0) and (ii < file_names2.shape[0]):
                image_path_2=os.path.join(folder_path_2,file_names2[ii])
                neg_image.append(displacement(image_path_1,image_path_2))

                #filename="%s_%s"%(i,ii) + ".png"
                
                #neg_image=scipy.misc.toimage(neg_image)
                #print(filename)
                #neg_image.save(os.path.join(folder_path_to_save,filename))
            count=count+1

    return neg_image

                           