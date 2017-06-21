#!/usr/bin/python3
import os
import sys
import django
from time import sleep
from random import randint
import serial

sys.path.insert(0, os.path.abspath('../../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.log import log

from central.placaBase.overCAN import processaMensagem
from central.placaBase.placaBase import PlacaBase

# PlacaBase = PlacaBase()


def c(x):
    print(x)


PlacaBase.iniciar(PlacaBase, porta='/dev/ttyACM0', taxa=115200, callback=c)
tempo = 1

while(True):
    try:
        entrada = input()

        if(entrada == '1'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='ENDERECO', 4)
        if(entrada == '2'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='ENDERECO', 3)
        if(entrada == '3'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='INTERVALO_ENVIO', 10)
        if(entrada == '4'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='INTERVALO_ENVIO', 100)
        if(entrada == '5'):
        PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                               grandeza='ONLINE')
        if(entrada == '-'):
            PlacaBase.resetPlacaBase()

    except (KeyboardInterrupt):
        print("saindo, aguarde!")
        sleep(1)
        PlacaBase.fechar()
        exit()
