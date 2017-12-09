from django.contrib import admin
from .models import *
# Register your models here.


class RecordAdmin(admin.ModelAdmin):
    list_display = ('full_id','og_id','capm','tissue','panel','create_date')
    search_fields = ['full_id','og_id','capm']
admin.site.register(Record,RecordAdmin)
admin.site.register(Panel)
admin.site.register(Tissues)