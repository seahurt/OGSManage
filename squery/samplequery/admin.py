from django.contrib import admin
from .models import *
# Register your models here.


class RecordAdmin(admin.ModelAdmin):
    list_display = ('full_id', 'og_id', 'capm', 'tissue', 'panel',
                    'create_date', 'r1_size', 'r2_size', 'indb_date')
    search_fields = ['full_id', 'og_id', 'capm']


class OutDateAdmin(admin.ModelAdmin):
    list_display = ('record', 'isOutDated')
    search_fields = ['record']


admin.site.register(Record, RecordAdmin)
admin.site.register(Panel)
admin.site.register(Tissues)
admin.site.register(QC)
admin.site.register(OutDate, OutDateAdmin)
