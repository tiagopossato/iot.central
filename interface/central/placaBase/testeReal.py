#!/usr/bin/python3
import os
import sys
import django
from time import sleep
from random import randint
import serial

sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.log import log

from placaBase.overCAN import processaMensagem
from placaBase.placaBase import PlacaBase

pb = PlacaBase()
pb.iniciar('/dev/ttyAMA0', 115200, processaMensagem)
tempo = 1

while(True):
    try:
        pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))
        # for x in range(8):
        #     pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,1))
        #     sleep(tempo)
        # for x in range(8):
        #     pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
        sleep(tempo)
    except KeyboardInterrupt:
        for x in range(8):
            pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
        print("saindo, aguarde!")
        pb.fechar()
        exit()

while(False):
    try:
        entrada = input()

        if(entrada == '1'):
            pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,1))
        if(entrada == '2'):
            pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,0))
        if(entrada == '3'):
            pb.enviaComando('3', 'CHANGE_SEND_TIME', "1")
            pb.enviaComando('2', 'CHANGE_SEND_TIME', "1")
        if(entrada == '4'):
            pb.enviaComando('3', 'CHANGE_SEND_TIME', "255")
            pb.enviaComando('2', 'CHANGE_SEND_TIME', "255")
        if(entrada == '5'):
            pb.enviaComando('0', 'IS_ONLINE')
        if(entrada == '-'):
            pb.resetPlacaBase()

    except (KeyboardInterrupt):
        for x in range(8):
            pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
        print("saindo, aguarde!")
        sleep(1)
        pb.fechar()
        exit()

def pbTeste():
    pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))

def pbOff():
    for x in range(8):
        pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
