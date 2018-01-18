#!python
"""
read in all samples' cfg file, judge and output which is newer data
"""
import re
import sys
import copy

if (len(sys.argv) != 4):
    sys.exit("Usage: python {0} <OG_all.cfg> <Newer.out.tsv> <log.txt>".format(sys.argv[0]))

f = open(sys.argv[1])
cfgs = f.readlines()
f.close()
allsample = dict()
IDS = []
OGIDS = set()
model_dict = {
    'Normal': {'ver': 0, 'capm': 0, 'r1': '', 'r2': '', 'panel': '', 'paneltype': '', 'panelver': 0, 'fullID': '', 'tissue': 'Normal'},
    'cfDNA': {'ver': 0, 'capm': 0, 'r1': '', 'r2': '', 'panel': '', 'paneltype': '', 'panelver': 0, 'fullID': '', 'tissue': 'cfDNA'},
    'FFPE': {'ver': 0, 'capm': 0, 'r1': '', 'r2': '', 'panel': '', 'paneltype': '', 'panelver': 0, 'fullID': '', 'tissue': 'FFPE'},
}
ff = open(sys.argv[3], 'wt')
for x in cfgs:
    ID, tissue, R1, R2, panel, paneltype = x.strip().split()
    panelversion = 0
    OGID = re.search('[O1]G[\d]+(OL[\d]+)*', ID).group(0)
    OGIDS.add(OGID)
    try:
        capm = re.search('CA-PM-([\d]+)', R1).group(1)
        capm = int(capm)
    except BaseException:
        # print("capm error for %s" % R1)
        capm = 0

    try:
        ver = re.search('[CNT]([\d])', ID).group(1)
        ver = int(ver)
    except BaseException:
        ver = 0
        # print("ver error for :%s" %ID)
    if 'b' in ID and 'M' not in ID and 'H' not in ID:
        try:
            panelversion = re.search('[\d]b([\d])', ID).group(1)
            panelversion = int(panelversion)
        except BaseException:
            # print("panel version error for:%s" %ID)
            panelversion = 0

    if OGID not in allsample:
        allsample[OGID] = copy.deepcopy(model_dict)
        # allsample[OGID][tissue]['ver'] = int(ver)
        # allsample[OGID][tissue]['capm'] = int(capm)
        # allsample[OGID][tissue]['r1'] = R1
        # allsample[OGID][tissue]['r2'] = R2
        # allsample[OGID][tissue]['panel'] = panel
        # allsample[OGID][tissue]['paneltype'] = paneltype
        # allsample[OGID][tissue]['fullID'] = ID

    if allsample[OGID][tissue]['ver'] > ver:
        msg = "based on version {0} was older than stored {1} ".format(ID, allsample[OGID][tissue]['fullID'])
        print(msg, file=ff, flush=True)
        continue
    elif allsample[OGID][tissue]['capm'] > capm:
        msg = "based on capm %s was older than stored %s" % (ID, allsample[OGID][tissue]['fullID'])
        print(msg, file=ff, flush=True)
        continue
    elif allsample[OGID][tissue]['panelver'] > panelversion:
        print("based on panel version %s was older than stored %s" % (ID, allsample[OGID][tissue]['fullID']), file=ff, flush=True)
        continue
    elif (allsample[OGID][tissue]['ver'] > ver and allsample[OGID][tissue]['capm'] > capm and
            allsample[OGID][tissue]['panelver'] > panelversion):
        print("identical %s vs %s" (allsample[OGID][tissue]['fullID'], ID), file=ff, flush=True)
        continue
    else:
        if allsample[OGID][tissue]['fullID'] != '':
            print("%s was newer than %s" % (ID, allsample[OGID][tissue]['fullID']), file=ff, flush=True)
        allsample[OGID][tissue]['ver'] = int(ver)
        allsample[OGID][tissue]['capm'] = int(capm)
        allsample[OGID][tissue]['r1'] = R1
        allsample[OGID][tissue]['r2'] = R2
        allsample[OGID][tissue]['panel'] = panel
        allsample[OGID][tissue]['paneltype'] = paneltype
        allsample[OGID][tissue]['fullID'] = ID
f.close()

with open(sys.argv[2], 'w') as pf:
    for ogid in allsample:
        for tissue in allsample[ogid]:
            if allsample[ogid][tissue]['fullID'] == '':
                continue
            outfield = ['fullID', 'tissue', 'r1', 'r2', 'panel', 'paneltype']
            outstr = [allsample[ogid][tissue][x] for x in outfield]
            print('\t'.join(outstr), file=pf)

print("%s OGID" % len(OGIDS))
