import os
import sys
import django
from time import sleep
from random import randint
import serial

sys.path.insert(0, os.path.abspath(os.path.join(__file__ ,"../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()
#importacoes depois do setup do django
from central.log import log
from central.placaBase.overCAN import processaMensagem
from central.placaBase.placaBase import PlacaBase
from central.models import Configuracoes

try:
    cfg = Configuracoes.objects.get()
    PlacaBase.iniciar(cfg.portaSerial, cfg.taxa, processaMensagem)

    while(True):
        try:
            for x in range(8):
                PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (2**x,))
                sleep(tempo)
            for x in range(8,-1,-1):
                PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (2**x,))
                sleep(tempo)
        except KeyboardInterrupt:
            encerrar()
except PermissionError as e:
    print("Executar como root!")
    print(e)
    exit()
except Exception as e:
    print(e)
    encerrar()
    exit()

def encerrar(arg1=0, arg2=0):
#    for x in range(8):
    PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,))
    log("RUN02","Encerrando aplicacao")
    PlacaBase.fechar(PlacaBase)
    exit()