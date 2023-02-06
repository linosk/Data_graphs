import os
import shutil
import zipfile

#Path to zipped data
raw_data_path = os.getcwd()
raw_data_path = raw_data_path[:raw_data_path.rfind("/")] + "/Raw_data"

#Path in which uzipped and sorted date will be placed
ready_data_path = os.getcwd() + "/Files"

#Delete "Files" directory if it exists
if os.path.exists(ready_data_path):
    shutil.rmtree(ready_data_path)

#Create "Files" directory if it does not exist
if not os.path.exists(ready_data_path):
    os.mkdir(ready_data_path)

#Define target zip file name located in raw_data_path that will be copied nad unzipped to directory "/Files" placed in ready_data_path
target_file = 'drive-download-20221017T162533Z-001.zip'

#Copy target file to "Files" directory
shutil.copy(raw_data_path+ "/" +target_file,ready_data_path)

#Change directory to "Files"
os.chdir(ready_data_path)
current_path = os.getcwd()

#Extract zipped file contents and then remove zipped file
handle = zipfile.ZipFile(target_file)
handle.extractall(current_path)
handle.close()
os.remove(target_file)

#Rename files names to be more readable
files = os.listdir(current_path)
for file in files:
    year=file[8:12]
    month=file[12:14]
    day=file[14:16]
    hour=file[16:18]
    minute=file[18:20]
    second=file[20:22]
    new_name = day+'.'+month+'.'+year+'-'+hour+':'+minute+':'+second+'.csv'
    #Trying to see whether not changing the data files into .csv files at this point will resolve the issue occuring later
    #new_name = day+'.'+month+'.'+year+'-'+hour+':'+minute+':'+second+'.txt'
    #new_name = day+'.'+month+'.'+year+'-'+hour+':'+minute+':'+second+'.xlsx'
    os.rename(file,new_name)

#Get list of files's names
files_renamed = os.listdir(current_path)
files_renamed.sort()

#Create directories used for sorting extracted files
lower_freq = "26GHz"
higher_freq = "38GHz"
noise = "Noise"
if os.path.exists(lower_freq):
    shutil.rmtree(lower_freq)
if os.path.exists(higher_freq):
    shutil.rmtree(higher_freq)
if os.path.exists(noise):
    shutil.rmtree(noise)
if not os.path.exists(lower_freq):
    os.mkdir(lower_freq)
if not os.path.exists(higher_freq):
    os.mkdir(higher_freq)
if not os.path.exists(noise):
    os.mkdir(noise)

#Sort files using created directories
i = 0
for file in files_renamed:
    if i<46:
        shutil.move(current_path+'/'+file,current_path+'/26GHz'+'/'+file)
    elif i>=46 and i<92:
        shutil.move(current_path+'/'+file,current_path+'/38GHz'+'/'+file)
    else:
        shutil.move(current_path+'/'+file,current_path+'/Noise'+'/'+file)
    i = i + 1