#!/usr/bin/python3
import os
import sys
import signal
from time import sleep
from random import randint
import serial
from threading import Thread

from central.log import log
from central.models import Configuracoes

from central.placaBase.overCAN import processaMensagem
from central.placaBase.placaBase import PlacaBase

tempo = 1

def encerrar(arg1=0, arg2=0):
#    for x in range(8):
    PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,))
    log("RUN02","Encerrando aplicacao")
    PlacaBase.fechar(PlacaBase)
    exit()

def app():    
    testaPlaca = _testaPlaca()
    testaPlaca.start()   

class _testaPlaca(Thread):
    def __init__ (self):
        Thread.__init__(self, name="Testa placa Base")

    def run(self):        
        log("RUN01","Iniciando aplicacao")
        
        cfg = Configuracoes.objects.get()
        PlacaBase.iniciar(cfg.portaSerial, cfg.taxa, processaMensagem)

        while(True):
            try:
                #pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))
                for x in range(8):
                    PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (2**x,))
                    sleep(tempo)
                for x in range(8,-1,-1):
                    PlacaBase.enviaComando('3', 'CHANGE_OUTPUT_STATE', (2**x,))
                    sleep(tempo)
            except KeyboardInterrupt:
                encerrar()
