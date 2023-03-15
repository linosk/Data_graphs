import os
import shutil
import re
import zipfile

curr_dir = os.getcwd()

sent_dir = curr_dir + '/Sent'

if os.path.exists(sent_dir):
    shutil.rmtree(sent_dir)

if not os.path.exists(sent_dir):
    os.mkdir(sent_dir)

plots_dir = curr_dir + '/Plots'

plots = os.listdir(plots_dir)
plots_to_sent = []

for plot in plots:
    if re.search(r"VER",plot) or re.search(r"HOR",plot):
        pass
    else:
        shutil.move(f'{plots_dir}/{plot}',f'{sent_dir}/{plot}')

shutil.move(f'{curr_dir}/CorrEff.txt',f'{sent_dir}/CorrEff.txt')

with zipfile.ZipFile("Sent.zip",'w',zipfile.ZIP_DEFLATED) as newzip:
    for dirpath, dirnames, files in os.walk('Sent'):
        for file in files:
            newzip.write(os.path.join(dirpath,file))