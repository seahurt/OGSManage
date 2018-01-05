#!python3
import re
import os
import sys

def init():
    scriptPath = os.path.abspath(sys.argv[0])
    dirname = os.path.dirname(scriptPath)
    sys.path = ['', 
    '/lustre/project/og03/Galaxy/Tumor_galaxy/Dependence/Python36/lib/python36.zip', 
    '/lustre/project/og03/Galaxy/Tumor_galaxy/Dependence/Python36/lib/python3.6', 
    '/lustre/project/og03/Galaxy/Tumor_galaxy/Dependence/Python36/lib/python3.6/lib-dynload', 
    '/lustre/project/og03/Galaxy/OGSManage/.venv/lib/python3.6/site-packages']
    sys.prefix = '/lustre/project/og03/Galaxy/OGSManage/.venv'
    os.chdir(dirname)
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'squery.settings'
    django.setup()
