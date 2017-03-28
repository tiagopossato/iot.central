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

# PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_OUTPUT_STATE', (256,))
# PlacaBase.fechar(PlacaBase)
# exit()

while(False):
    try:
        PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_OUTPUT_STATE', (randint(0,255),))
        # for x in range(8):
        #     PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,1))
        #     sleep(tempo)
        # for x in range(8):
        #     PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
        sleep(tempo)
    except KeyboardInterrupt:
        PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_OUTPUT_STATE', (0,))
#        for x in range(8):
#            PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
        print("saindo, aguarde!")
        PlacaBase.fechar(PlacaBase)
        exit()

while(True):
    try:
        entrada = input()

        if(entrada == '1'):
            PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_ID', '50')
        if(entrada == '2'):
            PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_OUTPUT_STATE', (0,))
        if(entrada == '3'):
            PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_SEND_TIME', "10")
        if(entrada == '4'):
            PlacaBase.enviaComando(PlacaBase,'50', 'CHANGE_SEND_TIME', "255")
            PlacaBase.enviaComando(PlacaBase,'50', 'CHANGE_SEND_TIME', "255")
        if(entrada == '5'):
            PlacaBase.enviaComando(PlacaBase,'50', 'IS_ONLINE')
        if(entrada == '-'):
            PlacaBase.resetPlacaBase(PlacaBase)

    except (KeyboardInterrupt):
        PlacaBase.enviaComando(PlacaBase,'3', 'CHANGE_OUTPUT_STATE', (0,))
        print("saindo, aguarde!")
        sleep(1)
        PlacaBase.fechar(PlacaBase)
        exit()