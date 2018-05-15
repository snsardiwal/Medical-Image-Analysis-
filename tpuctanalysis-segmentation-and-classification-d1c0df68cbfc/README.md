## Segmentation and classification scripts to analyze lung CT data  

### How to use  

#### Prerequisites  
- Python 3.6  
- It is recomended to use python virtual environment to run the software. See the python venv link: https://docs.python.org/3/library/venv.html    
- It is recomended to use the software on an Ubuntu 16.04 machine (You can request for a full ready-to-use Virtual Machine with the repository)  

#### How to work with the repository  
The main idea is to use pull requests to work with the repository! It is important to track the repository changes by using this approach.  
The workflow is the following:  
0. There is the main branch on repository - `dev`. To make any changes you should create your own branch from the main branch.  
1. Go to the `Branches` menu on the Bitbucket repository and click `Create branch`.  
2. Select the `dev` branch to branch from and enter the name of you branch. It is recomended to name it according to feature you want to implement, e.g. `segment-size-calculation`  
3. Go to your local repository and checkout the new branch: ```git fetch; git checkout segment-size-calculation```.  
4. After the feature implementation you should to make a pull request to megre your changes to the `dev` branch. Make sure you have syncronized your local branch with the corresponding remote branch on the Bitbucket.  
5. Make a local merge with the `dev` branch: ```git pull origin dev```. Make sure the all megre conflicts have been resolved.  
6. Go to the Bitbucket repository, to the `Pull requests` menu and click `Create pull request`.  
7. Fill the form and click `Create pull request`.  
8. After that you can merge the changes: click the `Approve` button on the corresponding pull request page and after that click `Merge`.  

### How to run the scripts  

**To run the script to open a set of dicom files in the sertain thomography preset** you should run (inside the python 3.6 virtual environment):  
```python read_dicom_files.py [-i path/to/directory/contained/dicom/files] [-r wide|soft|lung|pleural|bone] [-o /path/to/output/directory] [-s number_to_exclude_slices_from_the_start] [-e number_to_exclude_slices_from_the_end] [-h_l] [-h_b]```  
By default: only the -i and -o arguments are required. -r by default equal to wide, -s equal to 0, -e equal to 0. Boolean arguments -h_l (highlight lung areas) and -h_b (highlight bone areas) by default equal to False.  
E.g. ```python read_dicom_files.py -i disseminated/19/20100216/ -r bone -o output_folder/ -s 2 -e 3 -h_l -h_b```  
Note: you can use ```python read_dicom_files.py -h``` to read the help messages.  

**To run the script to segment lungs for a set of dicom files and save them in a thomography preset** you should run (inside the python 3.6 virtual environment):  
```python segment_ct_slices.py [-i path/to/directory/contained/dicom/files] [-r wide|soft|lung|pleural|bone] [-o /path/to/output/directory] [-s number_to_exclude_slices_from_the_start] [-e number_to_exclude_slices_from_the_end]```  
By default: only the -i and -o arguments are required. -r by default equal to wide, -s equal to 0, -e equal to 0.  
Note: you can use ```python segment_ct_slices.py -h``` to read the help messages.  

**To run the script to create binary label masks and save them as NPY files** you should run (inside python 3.6 virtual environment):  
```python create_label_masks.py [-i path/to/directory/contained/label/images] [-m mode_of_label_representation] [-c main_color_of_labels_in_images] [-s seed_color_for_region_label_representation] [-l label_name] [-o path/to/directory/to/save/label_masks] [-v]```  
Label images should contain regions with borders or polygons to present label areas on the image. ```-m``` flag refers to the mode of label representation on the image: regions or polygons.  
Setting colors for labels on the images depends on the mode of representation: regions required color for region border color ```-c``` and color for seed inside a region ```-s```, polygons required only ```-c``` flag.  
```-l``` flag refers to the class of labels, e.g. 'disseminated'.  
Note: you can use ```python create_label_masks.py -h``` to read the help messages.  

**To run the script to extract GLCM texture features from dicom data considering class labels** you should run (inside python 3.6 virtual environment):  
```python extract_glcm_features.py [-i path/to/directory/contained/patients/data] [-w glcm_window_size] [-l glcm_levels_count] [-o path/to/directory/to/save/features/into/csv/file] [-v]```  
Patients directory should contain folders for patients (folder name - patient id), each patient folder should contain survey folders (folder name - survey id), each survey folder should contain folder for dicom data and folder for class label files.  
Output file is a CSV file.  
Note: you can use ```python extract_glcm_features.py -h``` to read the help messages.  
