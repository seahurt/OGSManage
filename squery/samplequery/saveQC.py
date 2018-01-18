from samplequery.models import Record, QC
# from django.core.exceptions import ObjectDoesNotExist


def saveqc(info):
    # print(info)
    fid = info.split()[0]
    fid = fid.split('-')[0]
    # print(fid)
    record = Record.objects.get(full_id=fid)
    if hasattr(record, 'qc'):
        raise ValueError("QC already exists")
    else:
        q = QC(record=record, qcinfo=info)
        q.save()
