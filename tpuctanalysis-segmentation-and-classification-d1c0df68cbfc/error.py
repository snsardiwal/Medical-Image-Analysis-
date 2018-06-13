import csv
import pandas as pd 
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np




def calculateError(path_to_file,best_diff=1):

	df = pd.read_csv(path_to_file,header=None)
	df.columns = ["Image 1","Image 2","Dissimilarity(before)","Dissimilarity(after)"]

	mod=df['Image 2'].sub(df['Image 1'], axis=0)
	mod=mod.sub(best_diff,axis=0)
	count=mod.astype(bool).sum(axis=0)

	return count

def create_hist_from_csv(path_to_file):

	df = pd.read_csv(path_to_file, header = None)
	df.columns = ["Image 1","Image 2","Dissimilarity(before)","Dissimilarity(after)"]

	diff=df['Image 2'].sub(df['Image 1'], axis=0)
	weights=np.ones_like(diff)/float(len(diff))
	hist=plt.hist(diff,20,[-5,5], weights=weights)
	plt.xlabel('Difference')
	plt.ylabel('Percentage %')
	#plt.savefig(path_to_file+'hist.jpg')

	return diff

def create_global_hist(path_to_folder):

	norm_diff=[]
	for i in range(7):
		path_to_file=path_to_folder+'/patient%d/lung/dataS.csv'%(i+2)
		
		"""
		print(i)
		print('\n')
		print(path_to_file)
		print('\n')
		"""
		diff=create_hist_from_csv(path_to_file)
		lst=diff.tolist()

		max_occ=max(lst,key=lst.count)
		
		lst=[x-max_occ for x in lst]
		norm_diff.append(lst)

	norm_diff=[val for sublist in norm_diff for val in sublist]
	print(len(norm_diff))

	weights=np.ones_like(norm_diff)/float(len(norm_diff))
	bin_edges=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10]
	global_hist=hist=plt.hist(norm_diff,weights=weights,bins=bin_edges)
	plt.xlabel('X')
	plt.ylabel('Percentage %')
	plt.show()
	plt.savefig("global_hist")


path_to_file="/Users/sachin/Desktop/CT_Project/registration_data"

"""
count=calculateError(path_to_file,best_diff=1)
print(count)
"""
create_global_hist(path_to_file)
#create_hist_from_csv(path_to_file+'/patient8/lung/dataS.csv')