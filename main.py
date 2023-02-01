import os
import shutil
import re
import zipfile

raw_data_path = os.getcwd()
raw_data_path = raw_data_path[:raw_data_path.rfind("/")] + "/Raw_data"

ready_data_path = os.getcwd() + "/Files"

print(raw_data_path)
print(ready_data_path)


if os.path.exists(ready_data_path):
    shutil.rmtree(ready_data_path)

if not os.path.exists(ready_data_path):
    os.mkdir(ready_data_path)

target = raw_data_path + re.match("*.zip")
target = 'drive-download-20221017T162533Z-001.zip'

"""

shutil.copy(path.replace('Files','')+target,path+'\\'+target)

os.chdir(path)

path = os.getcwd()

handle = zipfile.ZipFile(target)

handle.extractall(path)

handle.close()

os.remove(target)

files = os.listdir(path)

for file in files:
    year=file[8:12]
    month=file[12:14]
    day=file[14:16]
    hour=file[16:18]
    minute=file[18:20]
    second=file[20:22]
    new_name = day+'.'+month+'.'+year+'-'+hour+';'+minute+';'+second+'.csv'
    os.rename(file,new_name)

lower_freq = path+"\\26GHz"
higher_freq = path+"\\38GHz"
noise = path+"\\Noise"

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


files = os.listdir(path)

files.remove('26GHz')
files.remove('38GHz')
files.remove('Noise')

i = 0

buffer = ''

lower_freq_phrase = ',#Center frequency [Hz]:,+2.60000000000E+010'

for file in files:
    text_file = open(file,'r')
    buffer = text_file.read()
    text_file.close()
    if not buffer.find(lower_freq_phrase) == -1:
        shutil.move(path+'\\'+file,path+'\\26GHz'+'\\'+file)
    else:
        if i<92:
            shutil.move(path+'\\'+file,path+'\\38GHz'+'\\'+file)
        else:
            shutil.move(path+'\\'+file,path+'\\Noise'+'\\'+file)
    i=i+1

    """