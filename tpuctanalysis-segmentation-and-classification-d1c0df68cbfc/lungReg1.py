from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image

#folder_path1="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient2/time1/000.png"
#folder_path2="/Users/sachin/Desktop/CT_Project/images/boneMaskAfterMedianFilter/patient2/time2/000.png"

folder_path1="/Users/sachin/Desktop/CT_Project/images/lungMask/patient2/time1/000.png"
folder_path2="/Users/sachin/Desktop/CT_Project/images/lungMask/patient2/time2/005.png"

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


#if len ( sys.argv ) < 4:
 #   print( "Usage: {0} <fixedImageFilter> <movingImageFile> <outputTransformFile>".format(sys.argv[0]))
  #  sys.exit ( 1 )


fixed = sitk.ReadImage(folder_path1, sitk.sitkFloat32)

moving = sitk.ReadImage(folder_path2, sitk.sitkFloat32)

initialTx = sitk.CenteredTransformInitializer(fixed, moving, sitk.AffineTransform(fixed.GetDimension()))

R = sitk.ImageRegistrationMethod()

R.SetShrinkFactorsPerLevel([3,2,1])
R.SetSmoothingSigmasPerLevel([2,1,1])

R.SetMetricAsJointHistogramMutualInformation(20)
R.MetricUseFixedImageGradientFilterOff()
R.MetricUseFixedImageGradientFilterOff()


R.SetOptimizerAsGradientDescent(learningRate=1.0,
                                numberOfIterations=100,
                                estimateLearningRate = R.EachIteration)
R.SetOptimizerScalesFromPhysicalShift()

R.SetInitialTransform(initialTx,inPlace=True)

R.SetInterpolator(sitk.sitkLinear)

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

R.SetMetricAsANTSNeighborhoodCorrelation(2)
R.MetricUseFixedImageGradientFilterOff()
R.MetricUseFixedImageGradientFilterOff()


R.SetShrinkFactorsPerLevel([3,2,1])
R.SetSmoothingSigmasPerLevel([2,1,1])

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


#sitk.WriteTransform(outTx,)

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

    cimg=sitk.GetArrayFromImage(cimg)
    cimg=Image.fromarray(cimg)
    cimg.save("002.png")
    