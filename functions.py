from math import log10

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