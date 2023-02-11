from math import log10

def find_lin_value(value):
    return pow(10,value/10)

def find_log_value(value):
    return 10*log10(value)

#a is a measured value that has to be multiply by -1. Then the gain of antennas have to be maid liner, and the sum of all three values has to 
#be turned into decibels.
def calculate_path_loss(a,gtx,grx):
    path_loss = -a + find_lin_value(gtx) + find_lin_value(grx)
    path_loss = find_log_value(path_loss)
    return path_loss

def find_title(scenario):
    if(scenario[0]=='2' and scenario[1]=='6'):
        band="26"
    else:
        band="38"

    if(scenario[2]=='L'):
        conditions="LOS"
    else:
        conditions="NLOS"

    distance=float(scenario[3:5])
    distance=distance/10
    distance=str(distance)

    if(scenario[5]=='T'):
        axis="czasu."
    else:
        axis="częstotliwości."

    title = "Wartość tłumienia propagacyjnego w paśmie "+band+"GHz"+", dla warunków "+conditions+", odległość miedzy antenami "+distance+" metrów, w zależności od "+axis
    return title