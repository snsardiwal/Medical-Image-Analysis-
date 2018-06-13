from __future__ import print_function

import SimpleITK as sitk
import sys
import os
from PIL import Image
from image_processing.listFileNamesInFolder import *
sys.path.insert(0,"/Users/sachin/Desktop/CT_Project/tpuctanalysis-segmentation-and-classification-d1c0df68cbfc/image_processing")
from listFileNamesInFolder import listFileNames
from returnRegisteredImage import *
from compareMask import *

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




def imageRegistration(image_path1,image_path2):

	fixed = sitk.ReadImage(image_path1, sitk.sitkFloat32)

	moving = sitk.ReadImage(image_path2, sitk.sitkFloat32)

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
		simg2=sitk.GetArrayFromImage(simg2)
	return cimg,simg2

def ImageRegFromFolder(folder_path1,folder_path2,file_to_write_large,file_to_write_small,folder_path_to_save,NumberOfImages=10):
	filenames1=listFileNames(folder_path1)
	filenames2=listFileNames(folder_path2)

	matchIndexAfterReg=np.empty(filenames1.shape[0])
	matchPixelCountAfterReg=np.empty(filenames1.shape[0])
    
	for index1 in range(filenames1.shape[0]):
        
		im1_path=os.path.join(folder_path1,filenames1[index1])
		im1_array=np.array(Image.open(im1_path),dtype='uint8')
		count=-NumberOfImages//2
        
		while(count<NumberOfImages//2+1):
            
			index2=index1+count
            
			if count==-NumberOfImages//2:
				matchIndexAfterReg[index1]=index2
				matchPixelCountAfterReg[index1]=float('inf')

			if(index2>=0 and index2<filenames2.shape[0]):
                
				im2_path=os.path.join(folder_path2,filenames2[index2])
				im2_before_reg_array=np.array(Image.open(im2_path))
				cimg,im2_after_reg_array=imageRegistration(im1_path,im2_path)
				
				cimg=Image.fromarray(cimg)
				s="/%d_%d" % (index1,index2)+'.png'
				cimg.save(folder_path_to_save+s)
				pixelCountBeforeReg,negImageBefReg=compareImages(im1_array,im2_before_reg_array)
				pixelCountAfterReg,negImageAfterReg=compareImages(im1_array,im2_after_reg_array)

            
				string1="%03d %03d %d %d" % (index1,index2,pixelCountBeforeReg,pixelCountAfterReg)
				with open(file_to_write_large,'a') as f:
					f.write(string1)
					f.write('\n')

				if pixelCountAfterReg<matchPixelCountAfterReg[index1]:
					matchIndexAfterReg[index1]=index2
					matchPixelCountAfterReg[index1]=pixelCountAfterReg

            
			count=count+1

		im2_pathMatch=os.path.join(folder_path2,"%03d"%(matchIndexAfterReg[index1])+".png")
		im2_arrayMatch=np.array(Image.open(im2_pathMatch),dtype='uint8')

		pixelCountBefRegMatch,negImageBefRegMatch=compareImages(im1_array,im2_arrayMatch)
		string2="%03d %03d %d %d" % (index1,matchIndexAfterReg[index1],pixelCountBefRegMatch,matchPixelCountAfterReg[index1])
		with open(file_to_write_small,'a') as f:
			f.write(string2)
			f.write('\n')

	return matchIndexAfterReg,matchPixelCountAfterReg

folder_path1="/Users/sachin/Desktop/CT_Project/images/boneLungMask/patient2/time1/000.png"
folder_path2="/Users/sachin/Desktop/CT_Project/images/boneLungMask/patient2/time2/005.png"
file_path1="/Users/sachin/Desktop/CT_Project/registration_data/patient1/boneLung/dataL.log"
file_path2="/Users/sachin/Desktop/CT_Project/registration_data/patient1/boneLung/dataS.log"
folder_path_to_save="/Users/sachin/Desktop/CT_Project/images/imagesAfterRegistration/boneLungMask/patient2/colormap"
NumberOfImages=10
#a,b=ImageRegFromFolder(folder_path1,folder_path2,file_path1,file_path2,folder_path_to_save,NumberOfImages)

a,b=imageRegistration(folder_path1,folder_path2)
a=Image.fromarray(a)
a.save('003.png')
