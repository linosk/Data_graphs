import pandas as pd
import functions as fn
import numpy as np
import matplotlib.pyplot as plt

gain26 = 14
gain38V = 13
gain38H = 15

#Read from csv file and skip first 28 liness
#df = pd.read_csv("Files/26GHz/13.09.2022-10:49:31.csv", skiprows=28, encoding_errors='ignore')
df = pd.read_csv("Files/38GHz/13.09.2022-12:03:25.csv", skiprows=28, encoding_errors='ignore')

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

#Copy column contiang the time of measurement
time = cdf['Unnamed: 3']
time = time[::2]
time = time.astype(float)
time = time.to_numpy()

#Copy dataframe contesnts and delete additional columns
ndf=cdf.drop(['Unnamed: 1','Unnamed: 2','Unnamed: 3'],axis=1)

#Find out the dataframe dimensions
row, col = ndf.shape

#Copy X axis values to turn it to 1d array
freq = ndf.columns
freq = freq.to_numpy()

#Change strings values to floats
for i in range(col):
    freq[i]=float(freq[i])

#Change dataframe to 2d array, change strings to floats, calculate path loss and round the outcome
roundto = 5
ndf=ndf.to_numpy()
for i in range(row):
    for j in range(col):
        ndf[i,j]=float(ndf[i,j])
        if scenario[0:2] == "26":
            ndf[i,j]=round(fn.calculate_path_loss(ndf[i,j],gain26,gain26),roundto)
        else:
            if i%2 == 0:
                ndf[i,j]=round(fn.calculate_path_loss(ndf[i,j],gain38V,gain38V),roundto)
            else:
                ndf[i,j]=round(fn.calculate_path_loss(ndf[i,j],gain38H,gain38H),roundto)

#print(len(values))
#print(len(mea))
#print(ndf[0][0])

#print(values)

new = int(row/2)

S31freq = [0] * col
S41freq = [0] * col
S31time = [0] * new
S41time = [0] * new

#Calculate mean for i-th column for the S31 scenario in relative to frequency
for i in range(col):
    S31freq[i] = np.mean((ndf[:,i])[0::2])

#Calculate mean for i-th column for the S41 scenario in relative to frequency
for i in range(col):
    S41freq[i] = np.mean((ndf[:,i])[1::2])

#Calculate mean for i-th row for the S31 scenario in relative to time
for i in range(new):
    S31time[i] = np.mean((ndf[i*2,:]))

#Calculate mean for i-th row for the S41 scenario in relative to time
for i in range(new):
    S41time[i] = np.mean((ndf[i*2+1,:]))

width = 10
height = 3

freq = freq/1e10

plt.figure(figsize=(width,height))
plt.plot(freq,S31freq)
plt.title("1."+scenario+"Vf")
plt.xlabel("Częstotliwość [GHz]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("1."+scenario+"Vf"+'.jpg')
plt.close()

plt.figure(figsize=(width,height))
plt.plot(freq,S41freq)
plt.title("2."+scenario+"Hf")
plt.xlabel("Częstotliwość [GHz]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("2."+scenario+"Hf"+'.jpg')
plt.close()

time = time/1000

plt.figure(figsize=(width,height))
plt.plot(time,S31time)
plt.title("3."+scenario+"Vt")
plt.xlabel("Czas pomiaru [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("3."+scenario+"Vt"+'.jpg')
plt.close()

plt.figure(figsize=(width,height))
plt.plot(time,S41time)
plt.title("4."+scenario+"Ht")
plt.xlabel("Czas pomiaru [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("4."+scenario+"Ht"+'.jpg')
plt.close()

"""
#measurement = 0
measurement = 198
plt.plot(values,ndf[measurement])
#plt.title(scenario+"---"+str(measurement))
#plt.title(fn.find_title(scenario))
plt.title(scenario+"V-V")

if(scenario[5]=='F'):
    plt.xlabel("Częstotliwość [GHz]")
else:
    plt.xlabel("Czas [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
###plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
##print(len(buff))
#plt.show()

#plt.savefig(scenario+'.png', dpi=500)
plt.savefig(scenario+"V-V"+'.jpg')
plt.close()

#measurement = 1
measurement = 199
plt.plot(values,ndf[measurement])
#plt.title(scenario+"---"+str(measurement))
#plt.title(fn.find_title(scenario))
plt.title(scenario+"V-H")

if(scenario[5]=='F'):
    plt.xlabel("Częstotliwość [GHz]")
else:
    plt.xlabel("Czas [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
###plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
##print(len(buff))
#plt.show()

#plt.savefig(scenario+'.png', dpi=500)
plt.savefig(scenario+"V-H"+'.jpg')
plt.close()
"""