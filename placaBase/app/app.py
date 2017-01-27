#!/usr/bin/python3
import time
import os
from placaBase import PlacaBase
import serial
from time import sleep
from random import randint
from log import log
from overCAN import digest

pb = PlacaBase()
pb.iniciar('/dev/ttyACM0', 115200, digest)
tempo = 5

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
    while(True):
        try:
            #envia valores aleatorios para a placa de expansao
            pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))
            sleep(tempo)
        except KeyboardInterrupt:
            for x in range(8):
                pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
            print("saindo, aguarde!")
            pb.fechar()
            log("RUN02","Encerrando aplicacao")
            exit()
