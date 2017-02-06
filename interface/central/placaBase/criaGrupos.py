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

new_group, created = Group.objects.get_or_create(name='Visualizador')
new_group.permissions.clear()
new_group.permissions.add(Permission.objects.get(codename='change_alarme'))
new_group.permissions.add(Permission.objects.get(codename='change_log'))

'''
new_group, created = Group.objects.get_or_create(name='Instalador')
new_group.permissions.clear()
new_group.permissions.add(Permission.objects.get(codename='change_alarme'))
new_group.permissions.add(Permission.objects.get(codename='change_log'))

new_group.permissions.add(Permission.objects.get(codename='add_alarmetipo'))
new_group.permissions.add(Permission.objects.get(codename='add_entradadigital'))
new_group.permissions.add(Permission.objects.get(codename='add_placaexpansaodigital'))

new_group.permissions.add(Permission.objects.get(codename='change_alarmetipo'))
new_group.permissions.add(Permission.objects.get(codename='change_entradadigital'))
new_group.permissions.add(Permission.objects.get(codename='change_placaexpansaodigital'))

new_group.permissions.add(Permission.objects.get(codename='delete_alarmetipo'))
new_group.permissions.add(Permission.objects.get(codename='delete_entradadigital'))
new_group.permissions.add(Permission.objects.get(codename='delete_placaexpansaodigital'))

new_group.permissions.add(Permission.objects.get(codename='add_ambiente'))
new_group.permissions.add(Permission.objects.get(codename='change_ambiente'))
new_group.permissions.add(Permission.objects.get(codename='delete_ambiente'))

new_group.permissions.add(Permission.objects.get(codename='add_configuracao'))
new_group.permissions.add(Permission.objects.get(codename='change_configuracao'))
new_group.permissions.add(Permission.objects.get(codename='delete_configuracao'))
'''


