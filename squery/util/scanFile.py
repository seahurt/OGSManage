#!python
"""
find out data from searching dirs
"""
import os
import pickle

BASEDIR = '/p299/raw/2016/PM/split/'

filedict = dict()
filePathList = []

for root, dirs, files in os.walk(BASEDIR, topdown=True, followlinks=True):
    for file in files:
        if not file.endswith('.gz'):
            continue
        fullpath = os.path.join(root, file)
        filePathList.append(fullpath)
        print("add ", fullpath)

print('filedict size', len(filedict.keys()))
print('fullpath size', len(filePathList))


os.system("mkdir -p ../pickle/")
with open('../pickle/filePathList.pickle', 'wb') as fpl:
    pickle.dump(filePathList, fpl)
with open('../pickle/filePathList.xls', 'w') as fx:
    for file in filePathList:
        fx.write(file + '\n')
