from time import sleep, time
import random

# Configurações para usar os models do django
import os
import sys
import django
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "central.settings"
django.setup()

from comunicacao.models import Mqtt
from aplicacao.models import Leitura


while(True):
    try:
        l = Leitura(valor=random.uniform(15.5, 31.9), grandeza_id=3302, 
                    ambiente_id='7f6a02a4-2bd1-4f87-a31b-69e0447a67b6',
                    sensor_id='1cd0aed1-68e5-481c-9fb7-d1fcf3f78aa1'
                    )
        l.save()
        try:
            print(l)
        except Exception:
            continue
        # sleep(random.uniform(1.5, 5.1))
        sleep(1)
    except KeyboardInterrupt:
        break

exit()