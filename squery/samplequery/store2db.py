from samplequery.models import Record,Panel,Tissues

def save2db(info):
    fullid,ogid,capm,r1,r2,t_name,p_name = info
    try:
        Record.objects.get(full_id=fullid)
    except BaseException as e:
        print(e)
        print(fullid,'not in db')
    record = Record()
    record.full_id=fullid
    record.og_id = ogid
    record.capm = capm
    record.r1 = r1
    record.r2 = r2
    try:
        t = Tissues.objects.get(tissue_short_name=t_name)
    except:
        print(t_name)
        raise KeyError
    if t is None:
        print(t_name)
        raise KeyError
    p = Panel.objects.get(panel_name=p_name)
    if p is None:
        raise KeyError
    record.tissue = t
    record.panel = p
    record.save()

def addPanel(info):
    name,path,ptype = info
    if not Panel.objects.get(panel_name=name):
        raise KeyError
    panel = Panel()
    panel.panel_name = name
    panel.panel_path = path
    panel.panel_type = ptype
    panel.save()

def addTissues(info):
    t_name = info[0]
    if not Tissues.objects.get(tissue_short_name=t_name):
        raise KeyError
    tissue = Tissues()
    tissue.tissue_short_name = t_name
    tissue.save()
