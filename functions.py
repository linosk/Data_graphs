from math import log10

def find_lin_value(value):
    return pow(10,value/10)

def find_log_value(value):
    return 10*log10(value)

#Logarithmic values passed, they are being converted to linear, then summed and after that the sum is reconverted to logarithmic value
#TEST
def calculate_path_loss(a,gtx,grx):
    #path_loss = find_lin_value(a) + find_lin_value(gtx) + find_lin_value(grx)
    #TEST
    path_loss = -a + find_lin_value(gtx) + find_lin_value(grx)
    path_loss = find_log_value(path_loss)
    return path_loss