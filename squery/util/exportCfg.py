#!python3
"""
export all record to cfg format
the format is as follows:
ID  TissueType R1 R2 PanelPath PanelType
"""
import os
import sys
import setup  # local module
# usage handle
if len(sys.argv) != 2:
    sys.exit("Usage: python {} <output.xls>".format(sys.argv[0]))
outfile = os.path.abspath(sys.argv[1])
# setup django env
setup.init()
from samplequery.models import Record


# began the business code
queryset = Record.objects.all()
# output fields
# fields = ["full_id",'og_id','tissue_id','capm','r1','r2','panel_id']
# output loop
with open(outfile,'w') as ef:
    for record in queryset:
        # outStr = [record.__dict__[x] for x in fields]
        ef.write('\t'.join(record.getcfg)+'\n')
