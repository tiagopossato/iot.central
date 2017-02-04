#!/usr/bin/python3
import os
import sys
import signal
import django
from time import sleep
from random import randint
import serial

sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.log import log

from overCAN import processaMensagem
from placaBase import PlacaBase
pb = PlacaBase()
tempo = 1

def encerrar(arg1=0, arg2=0):
    for x in range(8):
        pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
    print("saindo, aguarde!")
    pb.fechar()
    exit()

signal.signal(signal.SIGTERM, encerrar)

if __name__ == "__main__":
    try:
        arquivo = open("/var/run/central.pid","w")
        pid = os.getpid()
        arquivo.write(str(pid))
        print(pid)
        arquivo.close()
    except PermissionError as e:
        print("Executar como root!")
        print(e)
        exit()

    log("RUN01","Iniciando aplicacao")
    
    pb.iniciar('/dev/ttyACM0', 115200, processaMensagem)

    while(True):
        try:
            #pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))
            for x in range(8):
                pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,1))
                sleep(tempo)
            for x in range(8):
                pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
                sleep(tempo)
        except KeyboardInterrupt:
            encerrar()