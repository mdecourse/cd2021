import os
from pathlib import Path

# put this file outside 2021-03_2a_stage1 directory
files = []
# directory name
dname = "2021-03_2a_stage1"
# iterdir() iterate over the files in directory
paths = sorted(Path(dname).iterdir(), key=os.path.getmtime)
for i in paths:
    #os.fspath() eturn the file system representation of the path
    files.append(os.fspath(i))
#print(files)
i = 0
for fpath in files:
    # original file name is fname
    i += 1
    # new file name
    npath = os.path.join(dname, "cd2021_stage1_2a_g" + str(i) + ".mp4")
    #print(npath)
    os.rename(fpath, npath)


