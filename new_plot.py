import os
import pandas as pd
import numpy as np
from functions import make_plot, find_log_value, find_log_value_arr

CSV26Files = os.listdir("/home/me/Uni/Master/Graphs/Data_graphs/Files/26GHz")
CSV26Files.sort()

CSV38Files = os.listdir("/home/me/Uni/Master/Graphs/Data_graphs/Files/38GHz")
CSV38Files.sort()

CSVfilesgroups = [CSV26Files,CSV38Files]

gain = 14

def distance_plots(CSVfilesgroups, path1, path2):

    curr = os.getcwd()

    distance_LOS = [0.7,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0]

    distance_NLOS = [0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5]

    corr_26_LOS_AVG = 0
    corr_26_NLOS_AVG = 0

    corr_38_LOS_AVG = 0
    corr_38_NLOS_AVG = 0

    corr_26_LOS_STD = 0
    corr_26_NLOS_STD = 0

    corr_38_LOS_STD = 0
    corr_38_NLOS_STD = 0

    a = 0
    b = 0
    c = 0
    d = 0

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

            XPD_for_std_LOS = []
            XPD_for_std_NLOS = []

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

            XPD_for_std_LOS = []
            XPD_for_std_NLOS = []

        for CSV_file in CSVFiles:
            #Read from csv file and skip first 28 liness
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

            S31mean = [0] * col
            S41mean = [0] * col
            S31std = [0] * col
            S41std = [0] * col

            Sxpd = [0] *col

            XPD = [0] * col

            for i in range(col):
                S31mean[i] = np.mean((ndf[:,i])[0::2])
                S31std[i] = np.std((ndf[:,i])[0::2])

                S41mean[i] = np.mean((ndf[:,i])[1::2])
                S41std[i] = np.std((ndf[:,i])[1::2])

                XPD[i] = np.array(S41mean[i]) - np.array(S31mean[i])

            Sxpd = np.array(S41mean) - np.array(S31mean)

            print(f'{scenario[0]}{scenario[2]}AV{scenario[3:5]}')
            make_plot(S31mean,0,150,50,freq,f'{scenario[0]}{scenario[2]}AV{scenario[3:5]}')
            ##print(f'{scenario[0]}{scenario[2]}SV{scenario[3:5]}')
            ##make_plot(S31std,0,10,0,freq,f'{scenario[0]}{scenario[2]}SV{scenario[3:5]}')
            print(f'{scenario[0]}{scenario[2]}AH{scenario[3:5]}')
            make_plot(S41mean,0,150,50,freq,f'{scenario[0]}{scenario[2]}AH{scenario[3:5]}')
            #print(f'{scenario[0]}{scenario[2]}SH{scenario[3:5]}')
            #make_plot(S41std,0,10,0,freq,f'{scenario[0]}{scenario[2]}SH{scenario[3:5]}')

            # make_plot(average_LOS_H,average_LOS_V,120,50,distance_LOS,'2LAPDD')
            print(f'{scenario[0]}{scenario[2]}AH{scenario[3:5]}')
            make_plot(S31mean,S41mean,150,50,freq,f'{scenario[0]}{scenario[2]}AP{scenario[3:5]}')

            print(f'{scenario[0]}{scenario[2]}AX{scenario[3:5]}')
            make_plot(Sxpd,0,65,-25,freq,f'{scenario[0]}{scenario[2]}AX{scenario[3:5]}')
            #make_plot(XPD_for_std_LOS,0,45,-5,distance_LOS,'2LSXDD')
            #make_plot(xpd_LOS,0,45,-5,distance_LOS,'2LAXDD')

            VER = 0
            HOR = 0
            for i in range(col):
                if S41mean[i]>S31mean[i]:
                    HOR+=1
                else:
                    VER+=1

            #print(VER)
            #print(HOR)

            if scenario[0] == '2':
                if scenario[2] == 'L':
                    a+=1
                    corr_26_LOS_AVG += np.corrcoef(S31mean,S41mean)[0][1]
                    corr_26_LOS_STD += np.corrcoef(S31std,S41std)[0][1]
                else:
                    b+=1
                    corr_26_NLOS_AVG += np.corrcoef(S31mean,S41mean)[0][1]
                    corr_26_NLOS_STD += np.corrcoef(S31std,S41std)[0][1]
            else:
                if scenario[2] == 'L':
                    c+=1
                    corr_38_LOS_AVG += np.corrcoef(S31mean,S41mean)[0][1]
                    corr_38_LOS_STD += np.corrcoef(S31std,S41std)[0][1]
                else:
                    d+=1
                    corr_38_NLOS_AVG += np.corrcoef(S31mean,S41mean)[0][1]
                    corr_38_NLOS_STD += np.corrcoef(S31std,S41std)[0][1]

            #print(type(np.corrcoef(S31mean,S41mean)))
            #print(np.corrcoef(S31std,S41std)[0][0])
            #print(np.corrcoef(S31std,S41std)[0][1])
            #print(np.corrcoef(S31std,S41std)[1][0])
            #print(np.corrcoef(S31std,S41std)[1][1])

            S31mean_mean = np.mean(S31mean)
            S41mean_mean = np.mean(S41mean)
            S31std = np.std(S31mean)
            S41std = np.std(S41mean)

            XPD_XPD = np.std(XPD)

            if scenario[2] == 'L':
                average_LOS_V.append(S31mean_mean)
                average_LOS_H.append(S41mean_mean)
                std_LOS_V.append(S31std)
                std_LOS_H.append(S41std)

                XPD_for_std_LOS.append(XPD_XPD)
            else:
                average_NLOS_V.append(S31mean_mean)
                average_NLOS_H.append(S41mean_mean)
                std_NLOS_V.append(S31std)
                std_NLOS_H.append(S41std)

                XPD_for_std_NLOS.append(XPD_XPD)

        #corr_26_LOS_AVG = 0
        #corr_26_NLOS_AVG = 0
#
        #corr_38_LOS_AVG = 0
        #corr_38_NLOS_AVG = 0
#
        #corr_26_LOS_STD = 0
        #corr_26_NLOS_STD = 0
#
        #corr_38_LOS_STD = 0
        #corr_38_NLOS_STD = 0

        if CSVFiles == CSV26Files:

            make_plot(average_LOS_H,average_LOS_V,130,50,distance_LOS,'2LAPDD')
            make_plot(average_NLOS_H,average_NLOS_V,130,50,distance_NLOS,'2NAPDD')

            xpd_LOS = np.array(average_LOS_H) - np.array(average_LOS_V)
            xpd_NLOS = np.array(average_NLOS_H) - np.array(average_NLOS_V)

            make_plot(xpd_LOS,0,45,-5,distance_LOS,'2LAXDD')
            make_plot(xpd_NLOS,0,45,-5,distance_NLOS,'2NAXDD')

            make_plot(std_LOS_H,std_LOS_V,10,0,distance_LOS,'2LSPDD')
            make_plot(std_NLOS_H,std_NLOS_V,10,0,distance_NLOS,'2NSPDD')

            #xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            #xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            make_plot(XPD_for_std_LOS,0,45,-5,distance_LOS,'2LSXDD')
            make_plot(XPD_for_std_NLOS,0,45,-5,distance_NLOS,'2NSXDD')

        else:

            make_plot(average_LOS_H,average_LOS_V,130,50,distance_LOS,'3LAPDD')
            make_plot(average_NLOS_H,average_NLOS_V,130,50,distance_NLOS,'3NAPDD')

            xpd_LOS = np.array(average_LOS_H) - np.array(average_LOS_V)
            xpd_NLOS = np.array(average_NLOS_H) - np.array(average_NLOS_V)

            make_plot(xpd_LOS,0,45,-5,distance_LOS,'3LAXDD')
            make_plot(xpd_NLOS,0,45,-5,distance_NLOS,'3NAXDD')

            make_plot(std_LOS_H,std_LOS_V,10,0,distance_LOS,'3LSPDD')
            make_plot(std_NLOS_H,std_NLOS_V,10,0,distance_NLOS,'3NSPDD')

            #xpd_LOS = np.array(std_LOS_H) - np.array(std_LOS_V)
            #xpd_NLOS = np.array(std_NLOS_H) - np.array(std_NLOS_V)

            make_plot(XPD_for_std_LOS,0,45,-5,distance_LOS,'3LSXDD')
            make_plot(XPD_for_std_NLOS,0,45,-5,distance_NLOS,'3NSXDD')
    
    os.chdir(curr)

    file = open('CorrEff.txt','w')
    file.write('Wartość średnia współczynnika korelacji dla 26GHz, LOS, średnie tłumienie propagacyjne.')
    file.write(f'\n{corr_26_LOS_AVG/a}')
    file.write('\n\nWartość średnia współczynnika korelacji dla 26GHz, NLOS, średnie tłumienie propagacyjne.')
    file.write(f'\n{corr_26_NLOS_AVG/a}')

    file.write('\n\nWartość średnia współczynnika korelacji dla 38GHz, LOS, średnie tłumienie propagacyjne.')
    file.write(f'\n{corr_38_LOS_AVG/b}')
    file.write('\n\nWartość średnia współczynnika korelacji dla 38GHz, NLOS, średnie tłumienie propagacyjne.')
    file.write(f'\n{corr_38_NLOS_AVG/b}')

    file.write('\n\nWartość średnia współczynnika korelacji dla 26GHz, LOS, odchylenie standardowe.')
    file.write(f'\n{corr_26_LOS_STD/c}')
    file.write('\n\nWartość średnia współczynnika korelacji dla 26GHz, NLOS, odchylenie standardowe.')
    file.write(f'\n{corr_26_NLOS_STD/c}')

    file.write('\n\nWartość średnia współczynnika korelacji dla 38GHz, LOS, odchylenie standardowe.')
    file.write(f'\n{corr_38_LOS_STD/d}')
    file.write('\n\nWartość średnia współczynnika korelacji dla 38GHz, NLOS, odchylenie standardowe.')
    file.write(f'\n{corr_38_NLOS_STD/d}')
    file.close()

distance_plots(CSVfilesgroups,"/home/me/Uni/Master/Graphs/Data_graphs/Files/26GHz","/home/me/Uni/Master/Graphs/Data_graphs/Files/38GHz")