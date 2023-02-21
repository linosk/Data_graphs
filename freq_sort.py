import os
import pandas as pd

path26 = os.getcwd() + "/Files/26GHz"
path38 = os.getcwd() + "/Files/38GHz"

files26 = os.listdir(path26)
files38 = os.listdir(path38)

#Remove files containing measurements in relation to time domain
count = 0
os.chdir(path26)
for file in files26:
    try:
        df = pd.read_csv(file, skiprows=28, encoding_errors='ignore')
        scenario = df['Unnamed: 4'].values[1]
        if(scenario[5]=='F'):
            count+=1
        else:
            os.remove(file)
    except:
        os.remove(file)

count = 0
os.chdir(path38)
for file in files38:
    try:
        df = pd.read_csv(file, skiprows=28, encoding_errors='ignore')
        scenario = df['Unnamed: 4'].values[1]
        if(scenario[5]=='F'):
            count+=1
        else:
            os.remove(file)
    except:
        os.remove(file)