# Configurações para usar os models do django
import os
import sys
import django
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "central.settings"
django.setup()

from aplicacao.log import log
from aplicacao.models import Configuracoes
from aplicacao.placaBase.overCAN import processaMensagem
from aplicacao.placaBase.placaBase import PlacaBase

try:
    cfg = Configuracoes.objects.get()
    PlacaBase.iniciar(cfg.portaSerial, cfg.taxa, processaMensagem)
except Exception as e:
    log('CEN01.0', str(e))

log('START', 'Servico da central iniciado')

# while(True): ?????