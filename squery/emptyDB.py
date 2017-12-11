#!python
import django
import re
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'squery.settings'
# print(os.environ['DJANGO_SETTINGS_MODULE'])
django.setup()

from samplequery.models import Record

#allRecords = Record.objects.all()

#for r in allRecords:
#    r.delete()



