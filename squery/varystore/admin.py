from django.contrib import admin
from .models import Tumor, Gene, Site, Drug, Package, Patient, Sample, Snv, Cnv, DrugRecord
# Register your models here.

admin.site.register(Tumor)
admin.site.register(Gene)
admin.site.register(Site)
admin.site.register(Drug)
admin.site.register(Package)
admin.site.register(Patient)
admin.site.register(Sample)
admin.site.register(Snv)
admin.site.register(Cnv)
admin.site.register(DrugRecord)
