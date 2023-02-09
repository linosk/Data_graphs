import pandas as pd
import numpy as np

gain26 = 14
gain38A = 13.5
gain38B = 14.5

df = pd.read_csv("Files/26GHz/13.09.2022-10:48:03.csv", skiprows=28, encoding_errors='ignore')
#df = pd.read_csv("Files/26GHz/13.09.2022-10:49:31.csv", skiprows=28, encoding_errors='ignore')

cdf = df

for x in range(3,401,4):
    cdf = cdf.drop([x,x+1])

cdf=cdf.reset_index()
cdf=cdf.drop([0])
cdf=cdf.drop(['index','Unnamed: 0','Unnamed: 4','t [s] U f [Hz]:'],axis=1)

ndf=cdf.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3'],axis=1)

#print(ndf)
#print(df)

row, col = ndf.shape

values = ndf.columns
values = values.to_numpy()
#print(type(values[0]))

#col = len(values)
#print(length)

for i in range(col):
    values[i]=float(values[i])
    #print(values[i])
    #print(type(values[i]))

ndf=ndf.to_numpy()
#print(ndf)

for i in range(row):
    for j in range(col):
        ndf[i,j]=float(ndf[i,j])
        ndf[i,j]=-ndf[i,j]+gain26+gain38A

print(ndf)

print(df)