#!python

import pickle

exceptListFile = "/p299/user/og03/wangjianghao1706/django/squery/pickle/exceptList.pickle"
errdbFile = "/p299/user/og03/wangjianghao1706/django/squery/pickle/dberrorlist.pickle"


with open(exceptListFile,'rb') as ef:
    exceptList = pickle.load(ef)

with open(errdbFile,'rb') as ef:
    dberror = pickle.load(ef)
with open('parse.log','w') as log:
    for x in exceptList:
        log.write(x+'\n')
with open('db.log','w') as log:
    for y in dberror:
        log.write(y+'\n')
