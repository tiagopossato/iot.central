from threading import Thread
from queue import Queue
import serial
import simplejson
from central.log import log
from overCAN import ovcComands
from time import sleep, time
import signal
import sys
try:
    import RPi.GPIO as gpio
except RuntimeError as e:
    print(e)

CENTRAL_ID = 0

class PlacaBase():
    def __init__(self):
        try:
            self.isOnline = False
            self.bufferEnvio = Queue()
            self.tempoMinimoEnvio = 1 #tempo minimo entre uma mensagem e outra
            # Configurando GPIO
            gpio.setwarnings(False)
            gpio.cleanup()
            gpio.setmode(gpio.BCM)
            # Configurando a direcao do Pino
            gpio.setup(12, gpio.OUT) # Pino DTR da placaBase
            gpio.output(12, gpio.HIGH) #Pino de reset da placaBase sempre em HIGH
        except Exception as e:
            log("PLB00",str(e))

    def iniciar(self,porta,taxa,callback):
        try:
            #inicia thread que envia as mensagens para a placa base
            self._envia = _EnviaMensagens(self)
            self._envia.start()

        except Exception as e:
            log("PLB02", str(e))

    def enviaComando(self, id, comando, msg = ''):
        try:
            strComando = str(int(id))
            strComando += ':'
            strComando += str(ovcComands[comando])
            strComando += ':'
            if(isinstance(msg, str)):
                strComando += str(msg)
            elif(isinstance(msg, tuple)):
                for x in range(len(msg)):
                    strComando += str(msg[x]) + ":"
            else:
                log("PLB03.1","O parâmetro msg deve ser uma única string ou uma tupla de strings")
                return False
            self.bufferEnvio.put(strComando)
            #verifica se a thread está ativa
            if(self._envia.isAlive() == False):
                self._envia.run()

        except ValueError as e:
            log("PLB03.2",str(e))
        #except KeyError as e:
        #    log("PLB05",str(e))

    def resetPlacaBase(self):
        try:
            gpio.output(12, gpio.LOW)
            sleep(0.5)
            gpio.output(12, gpio.HIGH)
            log("PLB04.0","Resetando placaBase")
        except Exception as e:
            log("PLB04.1",str(e))

    def fechar(self):
        try:
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(0)
"""
Classe que será chamada via thread para enviar as mensagens para porta serial
Esta classe envia as mensagens do bufferEnvio do objeto placaBase respeitando
o tempo mínimo da placaBase
"""
class _EnviaMensagens(Thread):
    def __init__ (self, _placaBase):
        self.placaBase = _placaBase
        Thread.__init__(self)

    def run(self):
        print("Thread EnviaMensagens iniciou!")
        try:
            while(self.placaBase.bufferEnvio.empty() == False):
                # print("--------------------------------------")
                #print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                mensagem = self.placaBase.bufferEnvio.get() + '\n'
                # print("Thread EnviaMensagens -> " + mensagem)
                # print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                # print("--------------------------------------")
                # while(self.placaBase.portaSerial.isOpen() == False): pass
                # self.placaBase.portaSerial.write(bytes(mensagem, 'UTF-8'))
                sleep(self.placaBase.tempoMinimoEnvio)
            # sleep(0.0001) #evita que o processador vá a 100%
            print("Thread EnviaMensagens terminou!")
        except Exception as e:
            log("PLB06.0",str(e))
        except KeyboardInterrupt as e:
            self.exit()
