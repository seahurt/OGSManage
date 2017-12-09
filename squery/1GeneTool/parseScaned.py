#！python

import re
import os
import pickle
from samplequery import store2db
def run_dbtask(request):
    #!python
    pick = '/p299/user/og03/wangjianghao1706/django/squery/samplequery/filePathList.pickle'
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
        '8b':'panel8b'
    }

    tissueDict = {
        'CFD':'cfDNA',
        'FFPED':'FFPE',
        'FNAD':'FFPE',
        'LEUD':'Normal',
        'FRED':'FFPE',
        'HYTD':'FFPE',
        'HYCFD':'FFPE'
    }
    exceptList = []
    for file in filelist:
        dirname,basename = os.path.split(file)
        fullid,suffix = basename.split('_',1)
        if 'test' in basename:
            continue
        try:
            ogid = re.search('OG[\d]{5,}|OG[\d]+OL[\d]+',fullid).group(0)
            capm = re.search('(CA-PM-[\d]+|CA_PM_[\d]+)',dirname)
            if capm is None:
                capm = 'CA-PM-Lost'
            else:
                capm = capm.group(0)
            tissue = re.search('CFD|FFPED|FNAD|LEUD|FRED|HYTD|HYCFD',fullid).group(0)
            panel = re.search('[1-9]+b|M[b\d]+',fullid).group(0)

            tissue = tissueDict[tissue]
            panel = panelDict[panel]
            if 'R1' in suffix.upper():
                r1 = file
                r2 = None
            if 'R2' in suffix.upper():
                r2 = file
                r1 = None

            if fullid not in ogsample:
                ogsample[fullid] = dict()
            ogsample[fullid]['ogid'] = ogid
            ogsample[fullid]['tissue'] = tissue
            ogsample[fullid]['panel'] = panel
            ogsample[fullid]['capm'] = capm
            if r1:
                ogsample[fullid]['r1'] = r1
            if r2:
                ogsample[fullid]['r2'] = r2
        except:
            exceptList.append(file)
            continue
    with open('/p299/user/og03/wangjianghao1706/django/squery/samplequery/ogsample.pickle','wb') as og:
        pickle.dump(ogsample,og)
    print("%d file cannot be parse, which have been pickled to exceptList.pickle" %len(exceptList))
    with open('exceptList.pickle','wb') as ep:
        pickle.dump(exceptList,ep)

    dberrorlist = []
    for fullid in ogsample.keys():
        idtitle = ['ogid','capm','r1','r2','tissue','panel']
        infolist = [ogsample[fullid][x] for x in idtitle]
        infolist = [fullid]+infolist
        try:
            store2db.save2db(infolist)
        except BaseException as e:
            print(e)
            dberrorlist.append(fullid)
            continue
    print("%d record cannot be store to db, which have been pickled to dberrorlist.pickle" %(len(dberrorlist)))
    with open('/p299/user/og03/wangjianghao1706/django/squery/samplequery/dberrorlist.pickle','wb') as dp:
        pickle.dump(dberrorlist,dp)