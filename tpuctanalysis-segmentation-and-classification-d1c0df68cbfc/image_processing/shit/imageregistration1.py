from __future__ import print_function

import SimpleITK as sitk
import sys
import os
import numpy as np
import scipy.misc
from PIL import Image



def command_iteration(method) :
    print("{0:3} = {1:10.5f} : {2}".format(method.GetOptimizerIteration(),
                                   method.GetMetricValue(),
                                   method.GetOptimizerPosition()))


#if len ( sys.argv ) < 4:
 #   print( "Usage: {0} <fixedImageFilter> <movingImageFile> <outputTransformFile>".format(sys.argv[0]))
  #  sys.exit ( 1 )
im1 = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20121102/120.png"
im2 = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20130301/121.png"

LIST="/Users/sachin/Desktop/CT_Project/data1.tfm"
fixed = sitk.ReadImage(im1, sitk.sitkFloat32)

moving = sitk.ReadImage(im2, sitk.sitkFloat32)

R = sitk.ImageRegistrationMethod()
R.SetMetricAsMeanSquares()
R.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 100 )
R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
R.SetInterpolator(sitk.sitkLinear)

R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )

outTx = R.Execute(fixed, moving)

print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))

outfile=[]
sitk.WriteTransform(outTx,LIST)

if ( not "SITK_NOSHOW" in os.environ ):
   
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
    nda.save("image.png")
    #sitk.Show( cimg, "ImageRegistration1 Composition" )