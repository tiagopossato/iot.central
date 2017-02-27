#!/usr/bin/python3
import os
import sys
import django
import random
import time
sys.path.insert(0, os.path.abspath('../../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.placaBase.overCAN  import inputState, newLeitura

# for x in range(20):
newLeitura(_idRedeSensor=random.randint(1,2),_grandeza=71, _valor=random.uniform(20, 50))
print('')