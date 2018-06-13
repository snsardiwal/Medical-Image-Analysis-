from __future__ import print_function
import SimpleITK as sitk
import sys
import os
from PIL import Image
import SimpleITK as sitk

def returnMovingImage(transform, fixed_image, moving_image):
    """
    Write the given transformation to file, resample the moving_image onto the fixed_images grid and save the
    result to file.
    
    Args:
        transform (SimpleITK Transform): transform that maps points from the fixed image coordinate system to the moving.
        fixed_image (SimpleITK Image): resample onto the spatial grid defined by this image.
        moving_image (SimpleITK Image): resample this image.
        outputfile_prefix (string): transform is written to outputfile_prefix.tfm and resampled image is written to 
                                    outputfile_prefix.mha.
    """                             
    resample = sitk.ResampleImageFilter()
    resample.SetReferenceImage(fixed_image)
    
    # SimpleITK supports several interpolation options, we go with the simplest that gives reasonable results.     
    resample.SetInterpolator(sitk.sitkLinear)  
    resample.SetTransform(transform)
    out=resample.Execute(moving_image)

    simg1=sitk.Cast(sitk.RescaleIntensity(fixed_image),sitk.sitkUInt8)
    simg2=sitk.Cast(sitk.RescaleIntensity(out),sitk.sitkUInt8)
    cimg=sitk.Compose(simg1,simg2,simg1//2.+simg2//2.)

    cimg=sitk.GetArrayFromImage(cimg)
    simg2=sitk.GetArrayFromImage(simg2)

    return cimg,simg2


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