import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import shutil
from functions import make_plot

CSV26Files = os.listdir("/home/me/Uni/Master/Graphs/Data_graphs/Files/26GHz")
CSV26Files.sort()
#print(CSV26Files)

CSV38Files = os.listdir("/home/me/Uni/Master/Graphs/Data_graphs/Files/38GHz")
CSV38Files.sort()
#print(CSV38Files)

CSVfilesgroups = [CSV26Files,CSV38Files]

#CSVfilesgroups = [CSV26Files]

#CSVfi = ['13.09.2022-10:49:31.csv']

gain = 14

width = 12
height = 5
maxy = 120
miny = 50

def distance_plots(CSVfilesgroups, path1, path2):
    distance_LOS = [0.7,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0]

    average_LOS_V = []
    average_LOS_H = []

    std_LOS_V = []
    std_LOS_H = []

    distance_NLOS = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5]

    average_NLOS_V = []
    average_NLOS_H = []

    std_NLOS_V = []
    std_NLOS_H = []

    n = 0
    m = 0

    i = 0

    for CSVFiles in CSVfilesgroups:
        if CSVFiles == CSV26Files:
            os.chdir(path1)
            average_LOS_V = []
            average_LOS_H = []
            average_NLOS_V = []
            average_NLOS_H = []

            std_LOS_V = []
            std_LOS_H = []
            std_NLOS_V = []
            std_NLOS_H = []

        else:
            os.chdir(path2)
            average_LOS_V = []
            average_LOS_H = []
            average_NLOS_V = []
            average_NLOS_H = []

            std_LOS_V = []
            std_LOS_H = []
            std_NLOS_V = []
            std_NLOS_H = []

        for CSV_file in CSVFiles:
            #Read from csv file and skip first 28 liness
            df = pd.read_csv(CSV_file, skiprows=28, encoding_errors='ignore')

            #Copy dataframe contents
            cdf = df
        
            #Get type of scenario
            scenario = df['Unnamed: 4'].values[1]

            #i += 1
            #print(f'{i}.{scenario}')
            
            #Delete rows S32 and S42
            for x in range(3,401,4):
                cdf = cdf.drop([x,x+1])

            #Delete unnecessary columns
            cdf=cdf.reset_index()
            cdf=cdf.drop([0])
            cdf=cdf.drop(['index','Unnamed: 0','Unnamed: 4','t [s] U f [Hz]:'],axis=1)

            #Copy column contiang the time of measurement - not really important in this case, can ommit
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
                    ndf[i,j]=-ndf[i,j]+gain+gain
            

            freq = freq/1e10
            time = time/1000

            new = int(row/2)

            S31mean = [0] * col
            S41mean = [0] * col            

            #Calculate mean for i-th column for the S31 scenario in relative to frequency
            for i in range(col):
                S31mean[i] = np.mean((ndf[:,i])[0::2])
            
            #Calculate mean for i-th column for the S41 scenario in relative to frequency
            for i in range(col):
                S41mean[i] = np.mean((ndf[:,i])[1::2])

            #print(len(S31mean))
            #print(len(S41mean))

            S31mean_mean = np.mean(S31mean)
            S41mean_mean = np.mean(S41mean)
            S31std = np.std(S31mean)
            S41std = np.std(S41mean)

            if scenario[2] == 'L':
                average_LOS_V.append(S31mean_mean)
                average_LOS_H.append(S41mean_mean)
                std_LOS_V.append(S31std)
                std_LOS_H.append(S41std)
            else:
                average_NLOS_V.append(S31mean_mean)
                average_NLOS_H.append(S41mean_mean)
                std_NLOS_V.append(S31std)
                std_NLOS_H.append(S41std)

        if CSVFiles == CSV26Files:

            make_plot(average_LOS_H,average_LOS_V,120,50,distance_LOS,'2LA')
            make_plot(average_NLOS_H,average_NLOS_V,120,50,distance_NLOS,'2NA')

            xpd_LOS = np.array(average_LOS_H) - np.array(average_LOS_V)
            xpd_NLOS = np.array(average_NLOS_H) - np.array(average_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - wartość średnia, 26GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("26xpdLOS"+".jpg")
            plt.close()

            shutil.move("26xpdLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26xpdLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - wartość średnia, 26GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("26xpdNLOS"+".jpg")
            plt.close()

            shutil.move("26xpdNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26xpdNLOS.jpg")

        ###########################################################################################

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,std_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,std_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość odchylenia standardowego tłumienia propagacyjnego w zależności od odległości, 26GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("26STDLOS"+".jpg")
            plt.close()

            shutil.move("26STDLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26STDLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,std_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,std_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość odchylenia standardowego tłumienia propagacyjnego w zależności od odległości, 26GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("26STDNLOS"+".jpg")
            plt.close()

            shutil.move("26STDNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26STDNLOS.jpg")

            xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - odchylenie standardowe, 26GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("26STDxpdLOS"+".jpg")
            plt.close()

            shutil.move("26STDxpdLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26STDxpdLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - odchylenie standardowe, 26GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("26STDxpdNLOS"+".jpg")
            plt.close()

            shutil.move("26STDxpdNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26STDxpdNLOS.jpg")

            LOSCorr = pd.DataFrame(list(zip(average_LOS_H,average_LOS_V)),columns=['V-H','V-V'])
            CorrLOS = LOSCorr.corr(method='pearson')

            NLOSCorr = pd.DataFrame(list(zip(average_NLOS_H,average_NLOS_V)),columns=['V-H','V-V'])
            CorrNLOS = NLOSCorr.corr(method='pearson')

            stdLOSCorr = pd.DataFrame(list(zip(std_LOS_H,std_LOS_V)),columns=['std V-H','std V-V'])
            stdCorrLOS = stdLOSCorr.corr(method='pearson')

            stdNLOSCorr = pd.DataFrame(list(zip(std_NLOS_H,std_NLOS_V)),columns=['std V-H','std V-V'])
            stdCorrNLOS = stdNLOSCorr.corr(method='pearson')

            os.chdir("/home/me/Uni/Master/Graphs/Data_graphs")

            if os.path.exists("26Corr.txt"):
                os.remove("26Corr.txt")
            if not os.path.exists("26Corr.txt"):
                file = open("26Corr.txt","x")
                file.close()
                file = open("26Corr.txt","w")
                file.write("26GHz")


            file.write("\n\nWspółczynnik korelacji między V-V a V-H dla 26GHz, warunki LOS.")
            file.write("\n\n"+str(CorrLOS))
            file.write("\n\nWspółczynnik korelacji między V-V a V-H dla 26GHz, warunki NLOS.")
            file.write("\n\n"+str(CorrNLOS))
            file.write("\n\nWspółczynnik korelacji między std V-V a std V-H dla 26GHz, warunki LOS.")
            file.write("\n\n"+str(stdCorrLOS))
            file.write("\n\nWspółczynnik korelacji między std V-V a std V-H dla 26GHz, warunki NLOS.")
            file.write("\n\n"+str(stdCorrNLOS))

            file.close()

        else:

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,average_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,average_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości, 38GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość średnia tłumienia propagacyjengo [dB]")
            plt.ylim(ymax = maxy, ymin = miny)
            plt.savefig("38LOS"+".jpg")
            plt.close()

            shutil.move("38LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,average_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,average_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości, 38GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość średnia tłumienia propagacyjengo [dB]")
            plt.ylim(ymax = maxy, ymin = miny)
            plt.savefig("38NLOS"+".jpg")
            plt.close()

            shutil.move("38NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38NLOS.jpg")

            xpd_LOS = np.array(average_LOS_H) - np.array(average_LOS_V)
            xpd_NLOS = np.array(average_NLOS_H) - np.array(average_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - wartość średnia, 38GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("38xpdLOS"+".jpg")
            plt.close()

            shutil.move("38xpdLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38xpdLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - wartość średnia, 38GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("38xpdNLOS"+".jpg")
            plt.close()

            shutil.move("38xpdNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38xpdNLOS.jpg")

        ###########################################################################################

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,std_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,std_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość odchylenia standardowego tłumienia propagacyjnego w zależności od odległości, 38GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("38STDLOS"+".jpg")
            plt.close()

            shutil.move("38STDLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38STDLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,std_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,std_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość odchylenia standardowego tłumienia propagacyjnego w zależności od odległości, 38GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("38STDNLOS"+".jpg")
            plt.close()

            shutil.move("38STDNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38STDNLOS.jpg")

            xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - odchylenie standardowe, 38GHz, LOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("38STDxpdLOS"+".jpg")
            plt.close()

            shutil.move("38STDxpdLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38STDxpdLOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości - odchylenie standardowe, 38GHz, NLOS")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("38STDxpdNLOS"+".jpg")
            plt.close()

            shutil.move("38STDxpdNLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/38STDxpdNLOS.jpg")

            LOSCorr = pd.DataFrame(list(zip(average_LOS_H,average_LOS_V)),columns=['V-H','V-V'])
            CorrLOS = LOSCorr.corr(method='pearson')

            NLOSCorr = pd.DataFrame(list(zip(average_NLOS_H,average_NLOS_V)),columns=['V-H','V-V'])
            CorrNLOS = NLOSCorr.corr(method='pearson')

            stdLOSCorr = pd.DataFrame(list(zip(std_LOS_H,std_LOS_V)),columns=['std V-H','std V-V'])
            stdCorrLOS = stdLOSCorr.corr(method='pearson')

            stdNLOSCorr = pd.DataFrame(list(zip(std_NLOS_H,std_NLOS_V)),columns=['std V-H','std V-V'])
            stdCorrNLOS = stdNLOSCorr.corr(method='pearson')

            os.chdir("/home/me/Uni/Master/Graphs/Data_graphs")

            if os.path.exists("38Corr.txt"):
                os.remove("38Corr.txt")
            if not os.path.exists("38Corr.txt"):
                file = open("38Corr.txt","x")
                file.close()
                file = open("38Corr.txt","w")
                file.write("38GHz")


            file.write("\n\nWspółczynnik korelacji między V-V a V-H dla 38GHz, warunki LOS.")
            file.write("\n\n"+str(CorrLOS))
            file.write("\n\nWspółczynnik korelacji między V-V a V-H dla 38GHz, warunki NLOS.")
            file.write("\n\n"+str(CorrNLOS))
            file.write("\n\nWspółczynnik korelacji między std V-V a std V-H dla 38GHz, warunki LOS.")
            file.write("\n\n"+str(stdCorrLOS))
            file.write("\n\nWspółczynnik korelacji między std V-V a std V-H dla 38GHz, warunki NLOS.")
            file.write("\n\n"+str(stdCorrNLOS))

            file.close()


    

distance_plots(CSVfilesgroups,"/home/me/Uni/Master/Graphs/Data_graphs/Files/26GHz","/home/me/Uni/Master/Graphs/Data_graphs/Files/38GHz")

