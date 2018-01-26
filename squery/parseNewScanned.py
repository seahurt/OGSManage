#!python
import re
import os
import pickle
import sys
from datetime import date,datetime
import setup
setup.init()
from samplequery import store2db

if len(sys.argv)!=2:
    print("Usage: python {0} <file.pickle>".format(sys.argv[0]))
    sys.exit()

def run_dbtask():
    """
    1. load pickled file from sys argv
    2. extract full id from file name
    3. extract og id, panel, and tissue from full id
    4. extract capm, file size, file time
    5. pass info to store2db module

    6. log parsed file info(a dict) and dump to pickle/ogsample.pickle
    7. log parse error file and dump to pickle/exceptList.pickle
    8. log save2db error file and dump to pickle/dberrorlist.pickle
    """
    pick = sys.argv[1]
    with open(pick, 'rb') as p:
        filelist = pickle.load(p)

    ogsample = dict()

    panelDict = {
        '9b': 'panel9b',
        '3b': 'panel3b',
        '11b': 'panel11b',
        '1b': 'panel1b',
        'M7': 'lungcancer7',
        'M50': 'cancer50',
        'M78': 'cancer78',
        'Mb': 'brca',
        '14b': 'panel14b',
        '2b': 'panel2b',
        '8b': 'panel8b',
        'unknow': 'unknow'
    }

    tissueDict = {
        'CFD': 'cfDNA',
        'FFPED': 'FFPE',
        'FNAD': 'FFPE',
        'LEUD': 'Normal',
        'FRED': 'FFPE',
        'HYTD': 'FFPE',
        'HYCFD': 'cfDNA',
        'GD': 'gDNA',
    }
    parseExcept = dict()
    for file in filelist:
        dirname, basename = os.path.split(file)
        try:
            fullid, suffix = basename.split('_R', 1)
        except BaseException:
            parseExcept[file] = 'Cannot be splited'
            #print(file, "Cannot be splited")
            continue

        if 'test' in basename:
            parseExcept[file] = 'ignore test'
            continue
        try:
            ogid = re.search('OG[\d]{5,}|OG[\d]+OL[\d]+|HD[\d]+|1G[\d]+', fullid).group(0)
            capm = re.search('(CA-PM-[\d]+|CA_PM_[\d]+)', dirname)
            if capm is None:
                capm = 'CA-PM-Lost'
            else:
                capm = capm.group(0)
            tissue = re.search('CFD|FFPED|FNAD|LEUD|FRED|HYTD|HYCFD|GD', fullid).group(0)
            try:
                panel = re.search('[1-9]+b|M[b\d]+', fullid).group(0)
            except BaseException:
                panel = 'unknow'

            tissue = tissueDict[tissue]
            panel = panelDict[panel]
            if 'R1' in basename:
                r1 = file
                r1_size = os.path.getsize(file)
                r1_size = "%d" % (r1_size / 1000000)
                r1_createtime = datetime.utcfromtimestamp(os.path.getctime(file))
                r2 = None
            if 'R2' in basename:
                r2 = file
                r2_size = os.path.getsize(file)
                r2_size = "%d" % (r2_size / 1000000)
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
        except BaseException as e:
            parseExcept[file] = str(e)
            continue

    # write out parse error
    successLog = '../data/parsed_{0}.xls'.format(str(date.today()))
    with open(successLog, 'w') as og:
        for key in ogsample.keys():
            og.write('\t'.join([key]+[str(ogsample[key][x]) for x in ogsample[key]])+'\n')
    failParseLog = '../data/failParse_{0}.xls'.format(str(date.today()))
    print("%d file cannot be parse" % len(parseExcept))
    with open(failParseLog,'w') as ep:
        for key in parseExcept:
            ep.write('\t'.join([key]+[parseExcept[key]])+'\n')

    # store to db
    new_batch_fullid = []
    dberrorlist = dict()
    for fullid in ogsample.keys():
        idtitle = ['ogid', 'capm', 'r1', 'r2', 'tissue', 'panel', 'r1_size', 'r2_size', 'createtime']
        infolist = [ogsample[fullid][x] for x in idtitle]
        infolist = [fullid] + infolist
        try:
            store2db.save2db(infolist)
        except BaseException as e:
            #print(e)
            dberrorlist[fullid] = str(e)
            continue
        new_batch_fullid.append(fullid)
    # write out store to db error
    print("%d record cannot be store to db,saved to dberrorlist.pickle" % (len(dberrorlist)))
    dbfaillog = '../data/dbfail_{0}.xls'.format(str(date.today()))
    with open(dbfaillog, 'w') as dp:
        for key in dberrorlist.keys():
            dp.write(key+'\t'+dberrorlist[key]+'\n')
    new_batchid_file = '../data/fullid_batch_{0}.xls'.format(date.today())
    with open(new_batchid_file, 'w') as nbf:
        for id in new_batch_fullid:
            nbf.write(id+'\n')


if __name__ == '__main__':
    run_dbtask()
