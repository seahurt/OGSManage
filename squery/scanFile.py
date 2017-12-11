#!python
import os 
import pickle

BASEDIR = '/p299/raw/2016/PM/split/'

filedict = dict()
filePathList = []

for root,dirs,files in os.walk(BASEDIR,topdown=True,followlinks=True):
    #if 'CA' not in root:
    #    continue
    #if 'Reports' in root:
    #    continue
    #if 'html' in root:
    #    continue
    #print(root)
    for file in files:
        if not file.endswith('.gz'):
            continue
        fullpath = os.path.join(root,file)
        filePathList.append(fullpath)
        # fullid = file.split('_')[0]
        # if fullid not in filedict:
        #     filedict[fullid] = []
        # if fullpath not in filedict[fullid]:
        #     filedict[fullid].append(fullpath)
        print("add ",fullpath)

print('filedict size',len(filedict.keys()))
print('fullpath size',len(filePathList))

#with open('filedict.pickle','wb') as fd:
#    pickle.dump(filedict,fd)
with open('/p299/user/og03/wangjianghao1706/django/squery/pickle/filePathList.pickle','wb') as fpl:
    pickle.dump(filePathList,fpl)
with open('/p299/user/og03/wangjianghao1706/django/squery/pickle/filePathList.xls','w') as fx:
    for file in filePathList:
        fx.write(file+'\n')

