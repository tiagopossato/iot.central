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


# PlacaBase.iniciar(porta='/dev/ttyUSB0', taxa=115200, callback=processaMensagem)
tempo = 1
s = 1
while(True):
    try:
        entrada = input()

        if(entrada == '1'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL', grandeza='ENDERECO', valor=4)
        if(entrada == '2'):
            PlacaBase.enviaComando(idRede='4', tipoGrandeza='ESPECIAL',
                                   grandeza='ENDERECO', valor=3)
        if(entrada == '3'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='INTERVALO_ENVIO', valor=10)
        if(entrada == '4'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                                   grandeza='INTERVALO_ENVIO', valor=100)
        if(entrada == '5'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ESPECIAL',
                               grandeza='ONLINE')
        if(entrada == '6'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='SAIDA_DIGITAL',
                               grandeza='0', valor=int(s))
            s = not s
        if(entrada == '7'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='SAIDA_DIGITAL',
                               grandeza='1', valor=-1)
        if(entrada == '8'):
            PlacaBase.enviaComando(idRede='3', tipoGrandeza='ENTRADA_DIGITAL',
                               grandeza='1', valor=0)                       
        if(entrada == '-'):
            PlacaBase.resetPlacaBase()

    except (KeyboardInterrupt):
        print("saindo, aguarde!")
        sleep(1)
        PlacaBase.fechar()
        exit()
