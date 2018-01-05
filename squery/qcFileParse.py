#!python3
import sys
import setup # local module
# usage handle
if len(sys.argv)!=2:
    sys.exit("Usage: python {} <all.qc.xls>".format(sys.argv[0]))
qcfile = sys.argv[1]
# setup django env
setup.init()

from samplequery import saveQC

with open(qcfile) as q:
    for line in q.readlines():
        if 'Sample' in line:
            continue
        if line.strip() == '':
            continue
        try:
            saveQC.saveqc(line.strip())
        except ValueError as e:
            print(e)
        except:
            print("Something goes wrong for %s" %line.split('\t')[0])
        else:
            print("qc for %s saved" %line.split('\t')[0])
