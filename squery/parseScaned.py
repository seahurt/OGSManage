#!python
import django
import re
import os
import pickle
from datetime import datetime
os.environ['DJANGO_SETTINGS_MODULE'] = 'squery.settings'
print(os.environ['DJANGO_SETTINGS_MODULE'])
django.setup()
from samplequery import store2db
def run_dbtask():
    """
    1. load pickled file path list
    2. extract full id from file name
    3. extract og id, panel, and tissue from full id
    4. extract capm, file size, file time
    5. pass info to store2db module

    6. log parsed file info(a dict) and dump to pickle/ogsample.pickle
    7. log parse error file and dump to pickle/exceptList.pickle
    8. log save2db error file and dump to pickle/dberrorlist.pickle
    """
    #!python
    pick = 'pickle/filePathList.pickle'
    with open(pick,'rb') as p:
        filelist = pickle.load(p)

    ogsample = dict()

    panelDict= {
        '9b':'panel9b',
        '3b':'panel3b',
        '11b':'panel11b',
        '1b':'panel1b',
        'M7':'lungcancer7',
        'M50':'cancer50',
        'M78':'cancer78',
        'Mb':'brca',
        '14b':'panel14b',
        '2b':'panel2b',
        '8b':'panel8b',
        'unknow':'unknow'
    }

    tissueDict = {
        'CFD':'cfDNA',
        'FFPED':'FFPE',
        'FNAD':'FFPE',
        'LEUD':'Normal',
        'FRED':'FFPE',
        'HYTD':'FFPE',
        'HYCFD':'FFPE',
        'GD':'gDNA',

    }
    exceptList = []
    for file in filelist:
        dirname,basename = os.path.split(file)
        try:
            fullid,suffix = basename.split('_R',1)
        except:
            exceptList.append(file)
            print(file,"Cannot be splited")
            continue

        if 'test' in basename:
            exceptList.append(file)
            continue
        try:
            ogid = re.search('OG[\d]{5,}|OG[\d]+OL[\d]+|HD[\d]+|1G[\d]+',fullid).group(0)
            capm = re.search('(CA-PM-[\d]+|CA_PM_[\d]+)',dirname)
            if capm is None:
                capm = 'CA-PM-Lost'
            else:
                capm = capm.group(0)
            tissue = re.search('CFD|FFPED|FNAD|LEUD|FRED|HYTD|HYCFD|GD',fullid).group(0)
            try:
                panel = re.search('[1-9]+b|M[b\d]+',fullid).group(0)
            except:
                panel = 'unknow'

            tissue = tissueDict[tissue]
            panel = panelDict[panel]
            if 'R1' in basename:
                r1 = file
                r1_size = os.path.getsize(file)
                r1_size = "%d" % (r1_size/1000000)
                r1_createtime = datetime.utcfromtimestamp(os.path.getctime(file))
                r2 = None
            if 'R2' in basename:
                r2 = file
                r2_size = os.path.getsize(file)
                r2_size = "%d" % (r2_size/1000000)
                r2_createtime = datetime.utcfromtimestamp(os.path.getctime(file))
                r1 = None

            if fullid not in ogsample:
                ogsample[fullid] = dict()
            ogsample[fullid]['ogid'] = ogid
            ogsample[fullid]['tissue'] = tissue
            ogsample[fullid]['panel'] = panel
            ogsample[fullid]['capm'] = capm
            if r1:
                ogsample[fullid]['r1'] = r1
                ogsample[fullid]['r1_size'] = r1_size
                ogsample[fullid]['createtime'] = r1_createtime
            if r2:
                ogsample[fullid]['r2'] = r2
                ogsample[fullid]['r2_size'] = r2_size
                ogsample[fullid]['createtime'] = r2_createtime
        except:
            exceptList.append(file)
            print(file,'cannot be parsed!')
            continue

    # write out parse error
    with open('pickle/ogsample.pickle','wb') as og:
        pickle.dump(ogsample,og)
    print("%d file cannot be parse,saved to pickle/exceptList.pickle" %len(exceptList))
    with open('pickle/exceptList.pickle','wb') as ep:
        pickle.dump(exceptList,ep)

    # store to db
    dberrorlist = []
    for fullid in ogsample.keys():
        idtitle = ['ogid','capm','r1','r2','tissue','panel','r1_size','r2_size','createtime']
        infolist = [ogsample[fullid][x] for x in idtitle]
        infolist = [fullid]+infolist
        try:
            store2db.save2db(infolist)
        except BaseException as e:
            print(e)
            dberrorlist.append(fullid)
            continue
    # write out store to db error
    print("%d record cannot be store to db,saved to dberrorlist.pickle" %(len(dberrorlist)))
    with open('pickle/dberrorlist.pickle','wb') as dp:
        pickle.dump(dberrorlist,dp)
    with open('pickle/filelist.xls','w') as fx:
        for file in filelist:
            fx.write(file+'\n')


if __name__ == '__main__':
    run_dbtask()
