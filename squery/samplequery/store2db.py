from samplequery.models import Record,Panel,Tissues

def save2db(info):
    fullid,ogid,capm,r1,r2,t_name,p_name,r1_size,r2_size,create_date = info
    try:
        exist = Record.objects.get(full_id=fullid)
    except BaseException as e:
        print(e)
        print(fullid,'is ok to save')
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
    record = Record(full_id=fullid,
        og_id = ogid,
        capm = capm,
        r1 = r1,
        r2 = r2,
        tissue = t,
        panel = p,
        r1_size = r1_size,
        r2_size = r2_size,
        create_date = create_date
        )
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
