from math import log10
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import os
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

#TYPE FCVWDD
# Frequency: 2 or 3 - 26GHz or 38GHz
# Conditions: L or N - LOS or NLOS
# Values: A or S - average path loss or standard deviation of path loss
# What: P, X, V, H - what the plot will present, values for two polarization simultaneiusly, XPD values, average path loss for vertical polarization in the receiver antenna or average path loss for horizontal polarization in the receiver antenna
# Distance: if needed specify the distance between antennas in meters otherwise pass DD

def make_plot(y_axis_one, y_axis_two, maxy, miny, x_axis, type):
    width = 12
    height = 5
    path = os.getcwd()
    index = path.find('/Files')
    path = path[:index]
    path = path + '/Plots'
    plt.rcParams['font.size'] = 16

    if type[0] == '2':
        freg = '26'
    else:
        freg = '38'

    if type[1] == 'L':
        con = 'LOS'
    else:
        con = 'NLOS'

    if type[2] == 'A':
        if type[3] == 'P':
            if type[4] == 'D':
                yaxis_part = 'L'
                title_part = f'{yaxis_part} od d dla obu polaryzacji, '
                file_part = 'AVG_BOTH'
            else:
                distance = int(type[4]) + int(type[5])/10
                yaxis_part = 'L'
                title_part = f'{yaxis_part} odległość {distance}m dla obu polaryzacji, '
                file_part = f'AVG_BOTH_{type[4:]}'
        elif type[3] == 'X':
            if type[4] == 'D':
                yaxis_part = 'XPD'
                title_part = f'{yaxis_part} od d, '
                file_part = 'AVG_XPD'
            else:
                distance = int(type[4]) + int(type[5])/10
                yaxis_part = 'XPD'
                title_part = f'{yaxis_part} odległość {distance}m, '
                file_part = f'XPD_{type[4:]}'
        elif type[3] == 'V':
            distance = int(type[4]) + int(type[5])/10
            yaxis_part = 'L'
            title_part = f'{yaxis_part} polaryzacja V, odległość {distance}m, '
            file_part = f'AVG_VER_{type[4:]}'
        elif type[3] == 'H':
            distance = int(type[4]) + int(type[5])/10
            yaxis_part = 'L'
            title_part = f'{yaxis_part} polaryzacja H, odległość {distance}m, '
            file_part = f'AVG_HOR_{type[4:]}'

    #std
    else:
        if type[3] == 'P':
            yaxis_part = '$\u03C3_{L}$'
            title_part = f'{yaxis_part} od d dla obu polaryzacji, '
            file_part = 'STD_BOTH'
        elif type[3] == 'X':
            yaxis_part = '$\u03C3_{XPD}$'
            title_part = f'{yaxis_part} od d, '
            file_part = 'STD_XPD'
        elif type[3] == 'V':
            distance = int(type[4]) + int(type[5])/10
            yaxis_part = '$\u03C3_{L}$'
            title_part = f'{yaxis_part} polaryzacja V, odległość {distance}m, '
            file_part = f'STD_VER_{type[4:]}'
        elif type[3] == 'H':
            distance = int(type[4]) + int(type[5])/10
            yaxis_part = '$\u03C3_{L}$'
            title_part = f'{yaxis_part} polaryzacja H, odległość {distance}m, '
            file_part = f'STD_HOR_{type[4:]}'

    plt.figure(figsize=(width,height))

    if type[3] == 'P':
        if type[4] == 'D':
            plt.plot(x_axis,y_axis_one, marker='x', color='g',label='Pionowa-Pozioma')
            plt.plot(x_axis,y_axis_two, marker='o', color='r',label='Pionowa-Pionowa')
            plt.legend(loc='upper left')
        else:
            plt.plot(x_axis,y_axis_one, color='g',label='Pionowa-Poziowa')
            plt.plot(x_axis,y_axis_two, color='r',label='Pionowa-Pionowa')
            plt.legend(loc='upper left')
    #What: P, X, V, H
    elif type[3] == 'H' or type[3] == 'V':
        plt.plot(x_axis,y_axis_one)
    elif type[3] == 'X':
        if type[4] == 'D':
            plt.plot(x_axis,y_axis_one, marker='*')
        else:
            plt.plot(x_axis,y_axis_one)
    else:
        pass
        #plt.plot(x_axis,y_axis_one, marker='*')
        #plt.plot(x_axis,y_axis_one)

    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    #remove later
    #plt.title(f'{title_part}{freg}GHz, {con}')
    if (type[3] == 'P' and type[4] == 'D') or (type[3] == 'X' and type[4] == 'D'):
        if type[1] == 'L':
            plt.xlabel('$d_{LOS}$ [m]')
        else:
            plt.xlabel('$d_{NLOS}$ [m]')

    else:
        plt.xlabel('f [GHz]')
    plt.ylabel(f'{yaxis_part} [dB]')

    plt.xlim(left=x_axis[0])
    plt.xlim(right=x_axis[-1])
    plt.ylim(ymax=maxy, ymin=miny)
    plt.grid(which='major',linestyle='-',linewidth='0.5',color='black')
    plt.grid(which='minor',linestyle=':',linewidth='0.5',color='grey')
    plt.minorticks_on()
    file_name = f'{freg}_{con}_{file_part}.jpg'
    plt.savefig(file_name)
    plt.close()
    shutil.move(file_name,path+"/"+file_name)