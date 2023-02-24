import pandas as pd
import functions as fn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import os

gain26 = 14
gain38V = 13
gain38H = 15

CSV_files = ["Files/26GHz/13.09.2022-10:49:31.csv","Files/38GHz/13.09.2022-12:48:27.csv"]
for CSV_file in CSV_files:
    #Read from csv file and skip first 28 liness
    df = pd.read_csv(CSV_file, skiprows=28, encoding_errors='ignore')
    df = pd.read_csv(CSV_file, skiprows=28, encoding_errors='ignore')

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

    width = 12
    height = 5

    freq = freq/1e10
    time = time/1000

    new = int(row/2)

    S31freqMEAN = [0] * col
    S41freqMEAN = [0] * col
    S31timeMEAN = [0] * new
    S41timeMEAN = [0] * new

    #Calculate mean for i-th column for the S31 scenario in relative to frequency
    for i in range(col):
        S31freqMEAN[i] = np.mean((ndf[:,i])[0::2])

    #Calculate mean for i-th column for the S41 scenario in relative to frequency
    for i in range(col):
        S41freqMEAN[i] = np.mean((ndf[:,i])[1::2])

    #Calculate mean for i-th row for the S31 scenario in relative to time
    for i in range(new):
        S31timeMEAN[i] = np.mean((ndf[i*2,:]))

    #Calculate mean for i-th row for the S41 scenario in relative to time
    for i in range(new):
        S41timeMEAN[i] = np.mean((ndf[i*2+1,:]))

    plt.figure(figsize=(width,height))
    plt.plot(freq,S31freqMEAN)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wartość średnia tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Tłumienie propagacyjne [dB]")
    plt.savefig(fn.get_title_mean(scenario,"V","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(freq,S41freqMEAN)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wartość średnia tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Tłumienie propagacyjne [dB]")
    plt.savefig(fn.get_title_mean(scenario,"H","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S31timeMEAN)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wartość średnia tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Tłumienie propagacyjne [dB]")
    plt.savefig(fn.get_title_mean(scenario,"V","T")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S41timeMEAN)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wartość średnia tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Tłumienie propagacyjne [dB]")
    plt.savefig(fn.get_title_mean(scenario,"H","T")+".jpg")
    plt.close()

    #Lph - LpV

    a = fn.find_lin_value_arr(np.array(S31freqMEAN))
    b = fn.find_lin_value_arr(np.array(S41freqMEAN))
    c = fn.find_lin_value_arr(np.array(S31timeMEAN))
    d = fn.find_lin_value_arr(np.array(S41timeMEAN))

    LdiffF = np.array(b)-np.array(a)
    LdiffT = np.array(d)-np.array(c)

    LdiffF = fn.find_log_value_arr(np.array(LdiffF))
    LdiffT = fn.find_log_value_arr(np.array(LdiffT))

    plt.figure(figsize=(width,height))
    plt.plot(freq,LdiffF)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
    plt.title("Wykres różnicy tłumień")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Rożnica")
    plt.savefig(fn.get_title_diff(scenario,"F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,LdiffT)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
    plt.title("Wykres różnicy tłumień")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Rożnica")
    plt.savefig(fn.get_title_diff(scenario,"T")+".jpg")
    plt.close()

    #Var

    S31freqVAR = [0] * col
    S41freqVAR = [0] * col
    S31timeVAR = [0] * new
    S41timeVAR = [0] * new

    #Calculate var for i-th column for the S31 scenario in relative to frequency
    for i in range(col):
        S31freqVAR[i] = np.var((ndf[:,i])[0::2])

    #Calculate var for i-th column for the S41 scenario in relative to frequency
    for i in range(col):
        S41freqVAR[i] = np.var((ndf[:,i])[1::2])

    #Calculate var for i-th row for the S31 scenario in relative to time
    for i in range(new):
        S31timeVAR[i] = np.var((ndf[i*2,:]))

    #Calculate var for i-th row for the S41 scenario in relative to time
    for i in range(new):
        S41timeVAR[i] = np.var((ndf[i*2+1,:]))

    x = 1e3
    S31freqVAR = np.array(S31freqVAR)*x
    S41freqVAR = np.array(S41freqVAR)*x
    S31timeVAR = np.array(S31timeVAR)*x
    S41timeVAR = np.array(S41timeVAR)*x

    plt.figure(figsize=(width,height))
    plt.plot(freq,S31freqVAR)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wariancja wartości tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Wariancja")
    plt.savefig(fn.get_title_mean_var(scenario,"V","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(freq,S41freqVAR)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wariancja wartości tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Wariancja")
    plt.savefig(fn.get_title_mean_var(scenario,"H","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S31timeVAR)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wariancja wartości tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Wariancja")
    plt.savefig(fn.get_title_mean_var(scenario,"V","T")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S41timeVAR)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Wariancja wartości tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Wariancja")
    plt.savefig(fn.get_title_mean_var(scenario,"H","T")+".jpg")
    plt.close()

    #Std dev

    S31freqSTD = [0] * col
    S41freqSTD = [0] * col
    S31timeSTD = [0] * new
    S41timeSTD = [0] * new

    #Calculate std dev for i-th column for the S31 scenario in relative to frequency
    for i in range(col):
        S31freqSTD[i] = np.std((ndf[:,i])[0::2])

    #Calculate std dev for i-th column for the S41 scenario in relative to frequency
    for i in range(col):
        S41freqSTD[i] = np.std((ndf[:,i])[1::2])

    #Calculate std dev for i-th row for the S31 scenario in relative to time
    for i in range(new):
        S31timeSTD[i] = np.std((ndf[i*2,:]))

    #Calculate std dev for i-th row for the S41 scenario in relative to time
    for i in range(new):
        S41timeSTD[i] = np.std((ndf[i*2+1,:]))

    y = 1e3
    S31freqSTD = np.array(S31freqSTD)*y
    S41freqSTD = np.array(S41freqSTD)*y
    S31timeSTD = np.array(S31timeSTD)*y
    S41timeSTD = np.array(S41timeSTD)*y

    plt.figure(figsize=(width,height))
    plt.plot(freq,S31freqSTD)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Odchylenie standradowe wartości tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Odchylenie standardowe")
    plt.savefig(fn.get_title_mean_std(scenario,"V","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(freq,S41freqSTD)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Odchylenie standradowe wartości tłumienia propagacyjnego")
    plt.xlabel("Częstotliwość [GHz]")
    plt.ylabel("Odchylenie standardowe")
    plt.savefig(fn.get_title_mean_std(scenario,"H","F")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S31timeSTD)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Odchylenie standradowe wartości tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Odchylenie standardowe")
    plt.savefig(fn.get_title_mean_std(scenario,"V","T")+".jpg")
    plt.close()

    plt.figure(figsize=(width,height))
    plt.plot(time,S41timeSTD)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    plt.title("Odchylenie standradowe wartości tłumienia propagacyjnego")
    plt.xlabel("Czas pomiaru [s]")
    plt.ylabel("Odchylenie standardowe")
    plt.savefig(fn.get_title_mean_std(scenario,"H","T")+".jpg")
    plt.close()

    S31fregCorr = pd.DataFrame(list(zip(freq,S31freqMEAN)),columns=['Częst','TProp'])
    CorrS31F = S31fregCorr.corr(method='pearson')
    S41fregCorr = pd.DataFrame(list(zip(freq,S41freqMEAN)),columns=['Częst','TProp'])
    CorrS41F = S41fregCorr.corr(method='pearson')
    S31timeCorr = pd.DataFrame(list(zip(time,S31timeMEAN)),columns=['Czas','TProp'])
    CorrS31T = S31timeCorr.corr(method='pearson')
    S41timeCorr = pd.DataFrame(list(zip(time,S41timeMEAN)),columns=['Czas','TProp'])
    CorrS41T = S41timeCorr.corr(method='pearson')

    if scenario[0:2]=="26":
        if os.path.exists("Corr26.txt"):
            os.remove("Corr26.txt")
        if not os.path.exists("Corr26.txt"):
            file = open("Corr26.txt","x")
            file.close()
            file = open("Corr26.txt","w")
            file.write("26GHz")
    else:
        if os.path.exists("Corr38.txt"):
            os.remove("Corr38.txt")
        if not os.path.exists("Corr38.txt"):
            file = open("Corr38.txt","x")
            file.close()
            file = open("Corr38.txt","w")
            file.write("38GHz")

    file.write("\n\nScenariusz V-V, dziedzina częstotliwości")
    file.write("\n\n"+str(CorrS31F))
    file.write("\n\nScenariusz V-H, dziedzina częstotliwości")
    file.write("\n\n"+str(CorrS41F))
    file.write("\n\nScenariusz V-V, dziedzina czasu")
    file.write("\n\n"+str(CorrS31T))
    file.write("\n\nScenariusz V-H, dziedzina czsu")
    file.write("\n\n"+str(CorrS41T))

    file.close()