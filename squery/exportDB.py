#!python3
import re
import os
import sys
import setup # local module
# usage handle
if len(sys.argv)!=2:
    sys.exit("Usage: python {} <output.xls>".format(sys.argv[0]))
outfile = os.path.abspath(sys.argv[1])
# setup django env
setup.init()
from samplequery.models import Record

print("Warning:You are going to delete all the data in database!")
print("If you really want to do this, please open the file and uncomment the operation code")
# began the business code
# queryset = Record.objects.all()
# # output fields
# fields = ["full_id",'og_id','tissue_id','capm','r1','r2','panel_id']
# # output loop
# with open(outfile,'w') as ef:
#     for record in queryset:
#         outStr = [record.__dict__[x] for x in fields]
#         ef.write('\t'.join(outStr)+'\n')

