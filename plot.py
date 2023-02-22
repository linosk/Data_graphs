import pandas as pd
import functions as fn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

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

#Change dataframe to 2d array, change strings to floats, calculate path loss
ndf=ndf.to_numpy()
for i in range(row):
    for j in range(col):
        ndf[i,j]=float(ndf[i,j])
        if scenario[0:2] == "26":
            ndf[i,j]=fn.calculate_path_loss(ndf[i,j],gain26,gain26)

        else:
            if i%2 == 0:
                ndf[i,j]=fn.calculate_path_loss(ndf[i,j],gain38V,gain38V)
            else:
                ndf[i,j]=fn.calculate_path_loss(ndf[i,j],gain38H,gain38H)

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

width = 12
height = 5

freq = freq/1e10

plt.figure(figsize=(width,height))
plt.plot(freq,S31freq)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("1."+scenario+"Vf")
plt.xlabel("Częstotliwość [GHz]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("1."+scenario+"Vf"+'.jpg')
plt.close()


plt.figure(figsize=(width,height))
plt.plot(freq,S41freq)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("2."+scenario+"Hf")
plt.xlabel("Częstotliwość [GHz]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("2."+scenario+"Hf"+'.jpg')
plt.close()

time = time/1000

plt.figure(figsize=(width,height))
plt.plot(time,S31time)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("3."+scenario+"Vt")
plt.xlabel("Czas pomiaru [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("3."+scenario+"Vt"+'.jpg')
plt.close()

plt.figure(figsize=(width,height))
plt.plot(time,S41time)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("4."+scenario+"Ht")
plt.xlabel("Czas pomiaru [s]")
plt.ylabel("Tłumienie propagacyjne [dB]")
plt.savefig("4."+scenario+"Ht"+'.jpg')
plt.close()

#Lph - LpV
#from math import log10
LdiffF = np.array(S41freq) - np.array(S31freq)
#LdiffF = fn.find_lin_value(np.array(S41freq)) - fn.find_lin_value(np.array(S31freq))
#for i in range(len(LdiffF)):
#    LdiffF[i] = 10*log10(LdiffF[i])

LdiffT = np.array(S41time) - np.array(S31time)
#LdiffT = fn.find_lin_value(np.array(S41time)) - fn.find_lin_value(np.array(S31time))
#for i in range(len(LdiffT)):
#    LdiffT[i] = 10*log10(LdiffT[i])

plt.figure(figsize=(width,height))
plt.plot(freq,LdiffF)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("5."+scenario+"fDiff")
plt.xlabel("Częstotliwość [GHz]")
plt.ylabel("Rożnica tłumień [dB]")
plt.savefig("5."+scenario+"fDiff"+'.jpg')
plt.close()

plt.figure(figsize=(width,height))
plt.plot(time,LdiffT)
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
plt.title("6."+scenario+"tDiff")
plt.xlabel("Czas pomiaru [s]")
plt.ylabel("Rożnica tłumień [dB]")
plt.savefig("6."+scenario+"tDiff"+'.jpg')
plt.close()

#Correlation

CorrF = np.corrcoef(S31freq,S41freq)
CorrT = np.corrcoef(S31time,S41time)

print(len(CorrF))
print(len(CorrT))

#plt.figure(figsize=(width,height))
#plt.plot(freq,CorrF)
#plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
#plt.title("7.Współczynnik korelacji f")
#plt.xlabel("Częstotliwość [GHz]")
#plt.ylabel("Rożnica tłumień [dB]")
#plt.savefig("7.Współczynnik korelacji f"+'.jpg')
#plt.close()
#
#plt.figure(figsize=(width,height))
#plt.plot(time,CorrT)
#plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
#plt.title("8.Współczynnik korelacji t")
#plt.xlabel("Częstotliwość [GHz]")
#plt.ylabel("Czas pomiaru [s]")
#plt.savefig("8.Współczynnik korelacji t"+'.jpg')
#plt.close()