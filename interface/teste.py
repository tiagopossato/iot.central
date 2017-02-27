#!/usr/bin/python3
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.placaBase.overCAN  import inputState
