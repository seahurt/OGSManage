#!python
"""find patient name by give a id list file"""
import json
import sys
from repbin import get_md5_url
if sys.version_info.major!=3:
    sys.exit("Please use python3")

usage = """
python {0} <id.xls> <out.name.xls>
""".format(sys.argv[0])
if (len(sys.argv)<3):
    sys.exit(usage)
idXls = sys.argv[1]
nameXls = sys.argv[2]

names = open(nameXls,'w',encoding='utf-8')

idset = set()
with open(idXls) as f:
    for line in f.readlines():
        if 'OG' in line:
            idset.add(line.strip())

for Id in idset:
    print(Id)
    r = get_md5_url.SampleInfo(Id)
    if r.data['success']:
        info = json.dumps(r.data['data'],ensure_ascii=False)
        print("Success get info")
        print(info)
    else:
        info = 'No info'
        print("Cannot get info")
    # names.write()
    names.write('\t'.join([Id,info])+'\n')
    names.flush()
names.close()

# name
# gender
# age
# ID_number
# tumour_name
# doctor_name
# sample_list [{sample_type,sample_count,sample_unit,sampler_code,sampler_remarks,sampling_at,_id,}]
# hospital
# sample_receive_at
# report_at
# sortCodingName

