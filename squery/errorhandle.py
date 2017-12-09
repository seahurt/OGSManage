#!python

import pickle

exceptListFile = "/p299/user/og03/wangjianghao1706/django/squery/exceptList.pickle"
errdbFile = "/p299/user/og03/wangjianghao1706/django/squery/samplequery/dberrorlist.pickle"


with open(exceptListFile,'rb') as ef:
    exceptList = pickle.load(ef)

# with open(errdbFile,'rb') as ef:
#     dberror = pickle.load(ef)
with open('log','w') as log:
    for x in exceptList:
        log.write(x+'\n')
    # for y in dberror:
    #     log.write(y+'\n')