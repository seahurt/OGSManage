from samplequery.models import Record,QC

def saveqc(info):
    # print(info)
    fid = info.split()[0]
    fid = fid.split('-')[0]
    # print(fid)
    record = Record.objects.get(full_id=fid)
    print('record found!')
    try:
        record.qc
    except RelatedObjectDoesNotExist as e:
        q = QC(record=record,qcinfo=info)
        q.save()
    else:
        raise ValueError("QC already exists")


