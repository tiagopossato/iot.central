from time import sleep, time
import random

# Configuracoes para usar os models do django
import os
import sys
import django
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "central.settings"
django.setup()

from aplicacao.leitura import novaLeitura

grandezas = (3303, 3304)

while(True):
    try:
        idRede = random.randint(1, 2)
        grandeza = grandezas[random.randint(0, 1)]
        valor = random.uniform(15.5, 31.9) if grandeza == 3303 else random.uniform(75.5, 99.9)
        # Simula chegada de leitura analogica atraves da rede
        novaLeitura(_grandeza=grandeza, _idRede=idRede, _valor=valor)
        # sleep(random.uniform(1.5, 5.1))
        sleep(3)
    except KeyboardInterrupt:
        break

exit()