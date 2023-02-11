import pandas as pd
import functions as fn
import matplotlib.pyplot as plt

gain26 = 14
gain38A = 13.5
gain38B = 14.5

#Read from csv file and skip first 28 liness
#df = pd.read_csv("Files/26GHz/13.09.2022-10:48:03.csv", skiprows=28, encoding_errors='ignore')
#df = pd.read_csv("Files/26GHz/13.09.2022-10:51:35.csv", skiprows=28, encoding_errors='ignore')
#df = pd.read_csv("Files/26GHz/13.09.2022-10:56:19.csv", skiprows=28, encoding_errors='ignore')
#df = pd.read_csv("Files/26GHz/13.09.2022-11:44:59.csv", skiprows=28, encoding_errors='ignore')
df = pd.read_csv("Files/26GHz/13.09.2022-11:16:17.csv", skiprows=28, encoding_errors='ignore')

#Copy dataframe contents
cdf = df

#Get type of scenario
scenario = df['Unnamed: 4'].values[1]

#Delete rows S32 and S42
for x in range(3,401,4):
    cdf = cdf.drop([x,x+1])

#Delete unnecessary columns
cdf=cdf.reset_index()
cdf=cdf.drop([0])
cdf=cdf.drop(['index','Unnamed: 0','Unnamed: 4','t [s] U f [Hz]:'],axis=1)

#Copy dataframe contesnts and delete additional columns
ndf=cdf.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3'],axis=1)

#Find out the dataframe dimensions
row, col = ndf.shape

#Copy X axis values to turn it to 1d array
values = ndf.columns
values = values.to_numpy()

#Change strings values to floats
for i in range(col):
    values[i]=float(values[i])

#Change dataframe to 2d array, and change strings to floats
ndf=ndf.to_numpy()
for i in range(row):
    for j in range(col):
        ndf[i,j]=float(ndf[i,j])
        ndf[i,j]=fn.calculate_path_loss(ndf[i,j],gain26,gain26)

#print(ndf[:1])
#print(ndf)
measurement = 100
plt.plot(values,ndf[measurement])
#plt.title(scenario+"---"+str(measurement))
plt.title(fn.find_title(scenario))

if(scenario[5]=='F'):
    plt.xlabel("Częstotliwość [GHz]")
else:
    plt.xlabel("Czas [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
###plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
##print(len(buff))
#plt.show()

plt.savefig(scenario+'.png', dpi=500)