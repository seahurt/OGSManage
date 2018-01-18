#!python3
"""
set up django env for other stand alone module
"""
import os
import sys


def init():
    scriptPath = os.path.abspath('/lustre/project/og03/Galaxy/OGSManage/squery/util/')
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
