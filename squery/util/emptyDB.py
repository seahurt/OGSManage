#!python
import re
import sys
import os
import getpass
import setup

if sys.version_info.major!=3:
    sys.exit("Please use python3!")
setup.init()

from samplequery.models import Record
from django.contrib.auth import authenticate
  #
username = input("Username:")
passwd = getpass.getpass()
user =  authenticate(username=username,password=passwd)
if user:
    if user.is_superuser:
        print("This will delete all records in the database!")
        act = 'y' if input("Continue?[y/N]").lower()=='y' else 'n'
        if act == 'y':
            allRecords = Record.objects.all().delete()
            sys.exit("Action completed!")
        else:
            sys.exit("Action aborted!")
    else:
        sys.exit("Permission not allowed!")
else:
    sys.exit("Username/Password not match!")