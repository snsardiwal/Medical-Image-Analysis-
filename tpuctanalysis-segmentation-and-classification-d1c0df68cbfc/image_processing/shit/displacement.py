from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image
from save_transform_and_image import *



#if len (sys.argv) < 4:
 #   print( "Usage: {0} <fixedImageFilter> <movingImageFile> <outputTransformFile>".format(sys.argv[0]))
  #  sys.exit ( 1 )

im1 = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20121102/060.png"
im2 = "/Users/sachin/Desktop/CT_Project/images/bone_mask_after_median_filter/patient6/20130301/063.png"
LIST="/Users/sachin/Desktop/CT_Project/data1.tfm"


####################################################################################################################

#Read fixed and moving images
fixed = sitk.ReadImage(im1, sitk.sitkFloat32)
moving = sitk.ReadImage(im2, sitk.sitkFloat32)

############################################Registration 1############################################

#Initializing initial Tranformation
initialTx = sitk.CenteredTransformInitializer(fixed, moving, sitk.AffineTransform(fixed.GetDimension()))

#Image Registration Method
R = sitk.ImageRegistrationMethod()

R.SetShrinkFactorsPerLevel([3,2,1])
R.SetSmoothingSigmasPerLevel([2,1,1])

#Similarity metric Settings
R.SetMetricAsJointHistogramMutualInformation(30)
R.MetricUseFixedImageGradientFilterOff()
R.MetricUseFixedImageGradientFilterOff()

#Optimizer Settings
R.SetOptimizerAsGradientDescent(learningRate=1.0,
                                numberOfIterations=100,
                                estimateLearningRate = R.EachIteration)
R.SetOptimizerScalesFromPhysicalShift()

#Applying Initial Transformation
R.SetInitialTransform(initialTx,inPlace=True)

#Interpolator Settings
R.SetInterpolator(sitk.sitkLinear)

#Printing the results of every iteration
R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )
R.AddCommand( sitk.sitkMultiResolutionIterationEvent, lambda: command_multiresolution_iteration(R) )

#Adding Transformation form Registration 1 in outTx
outTx = R.Execute(fixed, moving)

#Printing the final results 
print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))

if ( not "SITK_NOSHOW" in os.environ ):
    save_transform_and_image(outTx,fixed,moving,'e_0001_1')


#Applying tranfomation on moving image
R.SetMovingInitialTransform(outTx)

############################################Registration 2############################################

displacementField = sitk.Image(fixed.GetSize(), sitk.sitkVectorFloat64)
displacementField.CopyInformation(fixed)
displacementTx = sitk.DisplacementFieldTransform(displacementField)
del displacementField
displacementTx.SetSmoothingGaussianOnUpdate(varianceForUpdateField=0.0,
                                            varianceForTotalField=1.5)


#Applying diplacement field initial transformation
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

#Adding tranformtion from Registration 2 in outTx
outTx.AddTransform( R.Execute(fixed, moving) )


#Printing the final Results
print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))


####################################################################################################################

#Writing transformation from outTx to an output file LIST
sitk.WriteTransform(outTx,  LIST)

#Applying
if ( not "SITK_NOSHOW" in os.environ ):
    save_transform_and_image(outTx,fixed,moving,'e_0003')




