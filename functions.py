from math import log10
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import shutil

def find_lin_value(value):
    return pow(10,value/10)

def find_log_value(value):
    return 10*log10(value)

def find_lin_value_arr(value):
    new_value = [0]*len(value)
    for i in range(len(value)):
        new_value[i] = pow(10,value[i]/10)

    return new_value

def find_log_value_arr(value):
    new_value = [0]*len(value)
    for i in range(len(value)):
        new_value[i] = 10*log10(value[i])

    return new_value

#a is a measured value that has to be multiply by -1. Then the gain of antennas have to be maid liner, and the sum of all three values has to 
#be turned into decibels.
def calculate_path_loss(a,gtx,grx):
    #ADD DECIBELS INSTEAD OF LINEAR VALUS
    path_loss = -a + find_lin_value(gtx) + find_lin_value(grx)
    path_loss = find_log_value(path_loss)
    return path_loss

def get_title_mean(scenario,pol,dom):
    title = ""
    title += scenario[0:2]+"-"
    title += scenario[2]+"-"
    title += scenario[3:5]+"-"
    if pol == "V":
        title += "V-"
    else:
        title += "H-"
    if dom == "F":
        title += "F"
    else:
        title += "T"

    return title

def get_title_diff(scenario,dom):
    title = ""
    title += "Diff-"
    title += scenario[0:2]+"-"
    title += scenario[2]+"-"
    title += scenario[3:5]+"-"
    if dom == "F":
        title += "F"
    else:
        title += "T"

    return title

def get_title_mean_var(scenario,pol,dom):
    title = ""
    title += "Var-"
    title += scenario[0:2]+"-"
    title += scenario[2]+"-"
    title += scenario[3:5]+"-"
    if pol == "V":
        title += "V-"
    else:
        title += "H-"
    if dom == "F":
        title += "F"
    else:
        title += "T"

    return title

def get_title_mean_std(scenario,pol,dom):
    title = ""
    title += "Std-"
    title += scenario[0:2]+"-"
    title += scenario[2]+"-"
    title += scenario[3:5]+"-"
    if pol == "V":
        title += "V-"
    else:
        title += "H-"
    if dom == "F":
        title += "F"
    else:
        title += "T"

    return title

#TYPE FCT
# Frequency 2 or 6 - 26GHz or 38GHz
# Conditions L or N - LOS or NLOS
# Type A, S, X, V, H, DD
# A - average path loss, 
# S - standard deviation of path loss, 
# X - XPD values, 
# V - receiver antenna has vertical polarization, 
# H - reciever antenna has horizontal polarization
# DDD - distance in meters
def make_plot(y_axis_one, y_axis_two, maxy, miny, x_axis, type):
    width = 12
    height = 5
    path = '/home/me/Uni/Master/Graphs/Data_graphs'

    plt.figure(figsize=(width,height))
    if type[2] == 'A' or type[2] == 'S':
        plt.plot(x_axis,y_axis_one, color='g',label='V-H')
        plt.plot(x_axis,y_axis_two, color='r',label='V-V')
    plt.legend(loc='upper left')
    #MAKE 2f MODIFABLE
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
    if type[0] == '2':
        freg = '26'
    else:
        freg = '38'
    if type[1] == 'L':
        con = 'LOS'
    else:
        con = 'NLOS'
    if type[2] == 'A':
        title_part = '\u03B1'
        file_part = 'AVG'
    plt.title(f'Wartość średnia {title_part} w zależności od d, {freg}GHz, {con}')
    if type[2] ==  'A' or type[2] == 'S':
        plt.xlabel('d [m]')
    if type[2] == 'A':
        plt.ylabel(f'{title_part} [dB]')
    plt.ylim(ymax=maxy, ymin=miny)
    file_name = f'{freg}{con}{file_part}.jpg'
    plt.savefig(file_name)
    plt.close()
    shutil.move(file_name,path+"/"+file_name)

    #if type == 'AVG':
    #    pass
    #elif type == 'STD':
    #    pass
    #else:
    #    pass

    #plt.figure(figsize=(width,height))
    #plt.plot(distance_LOS,average_LOS_H, color='g', label='V-H')
    #plt.plot(distance_LOS,average_LOS_V, color='r', label='V-V')
    #plt.legend(loc='upper left')
    #plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
    #plt.title("Wartość średnia tłumienia propagacyjnego w zależności od odległości, 26GHz, LOS")
    #plt.xlabel("Odległość [m]")
    #plt.ylabel("Wartość średnia tłumienia propagacyjengo [dB]")
    #plt.ylim(ymax = maxy, ymin = miny)
    #plt.savefig("26LOS"+".jpg")
    #plt.close()
    #shutil.move("26LOS.jpg","/home/me/Uni/Master/Graphs/Data_graphs/26LOS.jpg")