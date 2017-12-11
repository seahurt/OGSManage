from django.db import models
import os.path
# Create your models here.

class Tissues(models.Model):
    tissue_short_name = models.CharField('Tissue name',max_length=20,primary_key=True)
    tissue_full_name = models.CharField('Tissue full name',max_length=100,blank=True)
  
    def __str__(self):
        return self.tissue_short_name


class Panel(models.Model):
    panel_name = models.CharField('Panel name',max_length=50,primary_key=True)
    panel_path = models.CharField('Panel full path',max_length=500)
    panel_type = models.CharField('Panel type',max_length=20)
    panel_subtype = models.CharField('Panel subtype',max_length=20,default='unknown')

    def __str__(self):
        return self.panel_name

    def __was_exists(self):
        if os.path.exists(self.panel_path):
            return True
        else:
            return False

class Record(models.Model):
    full_id = models.CharField('Full ID',max_length=100,unique=True)
    og_id = models.CharField('OG ID',max_length=100)
    capm = models.CharField('CA-PM',max_length=100)
    r1 = models.CharField('R1',max_length=500)
    r2 = models.CharField('R2',max_length=500)
    tissue = models.ForeignKey(Tissues,on_delete=models.CASCADE)
    panel = models.ForeignKey(Panel,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_id

    def was_exists(self):
        if os.path.exists(self.r1) and os.path.exists(self.r2):
            return True
        else:
            return False
    @property
    def tissue_name(self):
        return self.tissue.tissue_short_name

    @property
    def panel_path(self):
        return self.panel.panel_path

    @property
    def panel_type(self):
        return self.panel.panel_type
    
    @property
    def panel_subtype(self):
        return self.panel.panel_subtype

    @property
    def panel_name(self):
        return self.panel.panel_name

    def getcfg(self):
        return(self.og_id,self.tissue_name,self.r1,self.r2,self.panel_path,self.panel_type)

