import os
import shutil

folders=["Files","__pycache__","Plots","Sent"]
for folder in folders:
    if os.path.exists(folder):
        shutil.rmtree(folder)

current_path=os.getcwd()
content=os.listdir(current_path)
for file in content:
    if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".zip") or file.endswith(".txt"):
        os.remove(os.path.join(current_path,file))
