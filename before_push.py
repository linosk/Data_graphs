import os
import shutil

files="Files"
if os.path.exists(files):
    shutil.rmtree(files)

pycache="__pycache__"
if os.path.exists(pycache):
    shutil.rmtree(pycache)

current_path=os.getcwd()
content=os.listdir(current_path)
for image in content:
    if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".zip"):
        os.remove(os.path.join(current_path,image))