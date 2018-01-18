#! python3
"""
Based on all id file and newer id file
mark records which not in newer id as outdated
"""
import setup
import sys
setup.init()
from samplequery.models import Record, OutDate


if (len(sys.argv) != 3):
    sys.exit("Usage: python {0} <allID> <newerID>".format(sys.argv[0]))
allID = [x.strip() for x in open(sys.argv[1]).readlines()]
pureID = [x.strip() for x in open(sys.argv[2]).readlines()]

for x in allID:
    r = Record.objects.get(full_id=x)
    outdate = OutDate(record=r)
    if x in pureID:
        outdate.isOutDated = False
    else:
        outdate.isOutDated = True
    outdate.save()
