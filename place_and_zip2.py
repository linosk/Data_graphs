import os
import shutil
import zipfile

target_dir = os.getcwd() + "/Plots"

if os.path.exists(target_dir):
    shutil.rmtree(target_dir)

if not os.path.exists(target_dir):
    os.mkdir(target_dir)

dir_26GHz = target_dir+"/26GHz"
dir_38GHz = target_dir+"/38GHz"

os.mkdir(dir_26GHz)
os.mkdir(dir_38GHz)

list_of_plots = []

list_of_files = os.listdir()

for file in list_of_files:
    if file.endswith(".jpg") or file.endswith(".txt"):
        list_of_plots.append(str(file))
    #if file.endswith(".txt"):
    #    shutil.move(os.getcwd()+"/"+file,target_dir+"/"+file)

for i in range(len(list_of_plots)):
    if (list_of_plots[i])[0:2] == "26":
        shutil.move(os.getcwd()+"/"+list_of_plots[i],dir_26GHz+"/"+list_of_plots[i])
    else:
        shutil.move(os.getcwd()+"/"+list_of_plots[i],dir_38GHz+"/"+list_of_plots[i])

target = "Plots"

with zipfile.ZipFile("Plots.zip",'w',zipfile.ZIP_DEFLATED) as newzip:
    for dirpath, dirnames, files in os.walk(target):
        for file in files:
            newzip.write(os.path.join(dirpath,file))