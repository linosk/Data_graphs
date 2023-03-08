import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import shutil

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

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,average_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,average_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość średnia tłumienia propagacyjengo [dB]")
            plt.ylim(ymax = maxy, ymin = miny)
            plt.savefig("26LOS"+".jpg")
            plt.close()

            shutil.move("26LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,average_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,average_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość średnia tłumienia propagacyjengo [dB]")
            plt.ylim(ymax = maxy, ymin = miny)
            plt.savefig("26NLOS"+".jpg")
            plt.close()

            shutil.move("26NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26NLOS.jpg")

            xpd_LOS = np.array(average_LOS_H) - np.array(average_LOS_V)
            xpd_NLOS = np.array(average_NLOS_H) - np.array(average_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("xpd26LOS"+".jpg")
            plt.close()

            shutil.move("xpd26LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/xpd26LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("xpd26NLOS"+".jpg")
            plt.close()

            shutil.move("xpd26NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/xpd26NLOS.jpg")

        ###########################################################################################

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,std_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,std_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("STD26LOS"+".jpg")
            plt.close()

            shutil.move("STD26LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STD26LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,std_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,std_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("STD26NLOS"+".jpg")
            plt.close()

            shutil.move("STD26NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STD26NLOS.jpg")

            xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("STDxpd26LOS"+".jpg")
            plt.close()

            shutil.move("STDxpd26LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STDxpd26LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("STDxpd26NLOS"+".jpg")
            plt.close()

            shutil.move("STDxpd26NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STDxpd26NLOS.jpg")

        else:

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,average_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,average_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości")
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
            plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości")
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
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("xpd38LOS"+".jpg")
            plt.close()

            shutil.move("xpd38LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/xpd38LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("Wartość współczynnika dyskryminacji polaryzacji skrośnej w zależności od odległości")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("xpd38NLOS"+".jpg")
            plt.close()

            shutil.move("xpd38NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/xpd38NLOS.jpg")

        ###########################################################################################

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,std_LOS_H, color='g', label='V-H')
            plt.plot(distance_LOS,std_LOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("STD38LOS"+".jpg")
            plt.close()

            shutil.move("STD38LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STD38LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,std_NLOS_H, color='g', label='V-H')
            plt.plot(distance_NLOS,std_NLOS_V, color='r', label='V-V')
            plt.legend(loc='upper left')
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość odchylenia standardowego [dB]")
            plt.ylim(ymax = 10, ymin = 0)
            plt.savefig("STD38NLOS"+".jpg")
            plt.close()

            shutil.move("STD38NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STD38NLOS.jpg")

            xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            plt.figure(figsize=(width,height))
            plt.plot(distance_LOS,xpd_LOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("STDxpd38LOS"+".jpg")
            plt.close()

            shutil.move("STDxpd38LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STDxpd38LOS.jpg")

            plt.figure(figsize=(width,height))
            plt.plot(distance_NLOS,xpd_NLOS)
            plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
            plt.title("TBD")
            plt.xlabel("Odległość [m]")
            plt.ylabel("Wartość współczynnika dyskryminacji polaryzacji skrośnej [dB]")
            plt.ylim(ymax = 45, ymin = -5)
            plt.savefig("STDxpd38NLOS"+".jpg")
            plt.close()

            shutil.move("STDxpd38NLOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/STDxpd38NLOS.jpg")


    

distance_plots(CSVfilesgroups,"/home/me/Uni/Master/Graphs/Data_graphs/Files/26GHz","/home/me/Uni/Master/Graphs/Data_graphs/Files/38GHz")

