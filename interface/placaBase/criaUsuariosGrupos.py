#!/usr/bin/python3
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from central.models import Alarme, Log
new_group, created = Group.objects.get_or_create(name='visualizador')
# Code to add permission to group visualizador
ct = ContentType.objects.get_for_model(Alarme)
permission = Permission.objects.create(codename='can_change_alarme',name='Can change Alarme',content_type=ct)
new_group.permissions.add(permission)

ct = ContentType.objects.get_for_model(Log)
permission = Permission.objects.create(codename='can_change_log',name='Can change Log',content_type=ct)
new_group.permissions.add(permission)
