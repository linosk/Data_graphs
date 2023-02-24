import os
import shutil

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

print(type(list_of_plots))

list_of_files = os.listdir()

for file in list_of_files:
    if file.endswith(".jpg"):
        list_of_plots.append(str(file))

for i in range(len(list_of_plots)):
    #print(list_of_plots[i])
    if (list_of_plots[i])[2:4] == "26" or (list_of_plots[i])[3:5] == "26":
        shutil.move(os.getcwd()+"/"+list_of_plots[i],dir_26GHz+"/"+list_of_plots[i])
    else:
        shutil.move(os.getcwd()+"/"+list_of_plots[i],dir_38GHz+"/"+list_of_plots[i])

"""
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
"""