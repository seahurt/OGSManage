from samplequery.models import Record,Panel,Tissues

def save2db(info):
    fullid,ogid,capm,r1,r2,t_name,p_name = info
    try:
        exist = Record.objects.get(full_id=fullid)
    except BaseException as e:
        print(e)
        print(fullid,'not in db')
    # full id validition
    else:
        # raise KeyError('Full id %s already in db' %fullid)
        return
    # t_name validition
    try:
        t = Tissues.objects.get(tissue_short_name=t_name)
    except:
        raise KeyError('%s is not a valid tissue name' %t_name)
    # p_name validition
    try:
        p = Panel.objects.get(panel_name=p_name)
    except:
        raise KeyError('%s is not a valid panel name' %t_name)
    record = Record()
    record.full_id=fullid
    record.og_id = ogid
    record.capm = capm
    record.r1 = r1
    record.r2 = r2   
    record.tissue = t
    record.panel = p
    record.save()

def addPanel(info):
    name,path,ptype = info
    try:
        exist = Panel.objects.get(panel_name=name)
    except:
        print("%s not in db, continue..." %name)
    else:
        raise KeyError("%s already in db" %name)
    panel = Panel()
    panel.panel_name = name
    panel.panel_path = path
    panel.panel_type = ptype
    panel.save()

def addTissues(info):
    t_name = info[0]
    try:
        Tissues.objects.get(tissue_short_name=t_name)
    except:
        print("%s not in db, continue")
    else:
        raise KeyError("%s already in db" %t_name)
    tissue = Tissues()
    tissue.tissue_short_name = t_name
    try:
        tissue_full_name = info[1]
    except IndexError:
        tissue_full_name = "Missing"
    tissue.save()
