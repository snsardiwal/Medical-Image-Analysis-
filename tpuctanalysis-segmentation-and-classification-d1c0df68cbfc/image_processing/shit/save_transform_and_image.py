from __future__ import print_function
import SimpleITK as sitk
import sys
import os
from PIL import Image

def returnMovingandColorImage(transform,fixed_image,moving_image,output_file_prefix):
	"""
    Write the given transformation to file, resample the moving_image onto the fixed_images grid and save the
    image
    
    Args:
        transform (SimpleITK Transform): transform that maps points from the fixed image coordinate system to the moving.
        fixed_image (SimpleITK Image): resample onto the spatial grid defined by this image.
        moving_image (SimpleITK Image): resample this image.
        outputfile_prefix (string): transform is written to outputfile_prefix.tfm and resampled image is written to 
                                    outputfile_prefix.mha.
    """                             

	resample=sitk.ResampleImageFilter()
	resample.SetReferenceImage(fixed_image)


	resample.SetInterpolator(sitk.sitkLinear)
	resample.SetTransform(transform)
	out=resample.Execute(moving_image)

	simg1 = sitk.Cast(sitk.RescaleIntensity(fixed_image), sitk.sitkUInt8)
	simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
	cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)

	nda = sitk.GetArrayViewFromImage(cimg)
	nda = Image.fromarray(nda)
	nda.save(output_file_prefix+'.png')