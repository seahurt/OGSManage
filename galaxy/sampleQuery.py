#!python
import sys
import requests

BaseURL = "http://192.168.1.215:9111/query/"
for x in range(len(sys.argv)):
    print(x)
    print(sys.argv[x])
output,Id,Id_type,tissue,panel,panelsubtype,outputIDFormat,dataset = sys.argv[1:]

o = open(output,'w')

if Id_type == 'og':
    full_id = []
    og_id = [x.strip() for x in Id.split('__cn__') if x.strip() !='']
elif Id_type == 'full':
    full_id = [x.strip() for x in Id.split('__cn__') if x.strip() !='']
    og_id = []


# full_id = [x.strip() for x in full_id.split('__cn__') if x.strip() !='']
# og_id = [x.strip() for x in og_id.split('__cn__') if x.strip() !='']
tissue = tissue.split(',')
panel = panel.split(',')
panelsubtype = panelsubtype.split(',')


qdict = dict()
qdict['full_id'] = full_id
qdict['og_id'] = og_id
qdict['tissue_name'] = tissue
qdict['panel_type'] = panel
qdict['panel_subtype'] = panelsubtype
if dataset == 'Regular':
    qdict['isOutDated'] = False
elif dataset == 'Deprecated':
    qdict['isOutDated'] = True
else:
    pass


for key in qdict.keys():
    if qdict[key]==[]:
        del qdict[key]
response = requests.post(BaseURL,json=qdict)
if response.status_code == 200:
    data = response.json()
else:
    data = []
    print(response.content)


fields = [outputIDFormat,'tissue_name','r1','r2','panel_path','panel_type']
for record in data:
    # data = json.loads(x)
    line = [record[x] for x in fields]
    o.write('\t'.join(line)+'\n')
o.close()



