from threading import Thread
from queue import Queue
import serial
import simplejson
from central.log import log
from placaBase.overCAN import ovcComands
from time import sleep, time
import signal
import sys
from random import randint

CENTRAL_ID = 0

class PlacaBase():
    def __init__(self):
        try:
            self.isOnline = False
            self.bufferEnvio = Queue()
            self.tempoMinimoEnvio = 0.02 #tempo minimo entre uma mensagem e outra
        except Exception as e:
            log("PLB00",str(e))

    def iniciar(self,porta,taxa,callback):
        try:
            #Inicia thread para receber as mensagens da placa base
            self._recebe = _RecebeMensagens(self, callback)
            self._recebe.start()
            #inicia thread que envia as mensagens para a placa base
            self._envia = _EnviaMensagens(self)
            self._envia.start()
            #inicia a thread que monitora se a placa está online
            # self._monitora = _MonitoraPlacaBase(self)
            # self._monitora.start()

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
            while(self.bufferEnvio.empty() == False): sleep(self.tempoMinimoEnvio)
            signal.pthread_kill(self._envia.ident, signal.SIGTERM)
            signal.pthread_kill(self._monitora.ident, signal.SIGTERM)
            signal.pthread_kill(self._recebe.ident, signal.SIGTERM)
            sleep(1)
            print("Aguardando threads terminarem")
            self._envia.join()
            self._monitora.join()
            self._recebe.join()
            self.portaSerial.close()
        except Exception as e:
            print(e)
            sys.exit(0)

"""
Classe que será chamada via thread para receber as mensagens da porta serial
"""
class _RecebeMensagens(Thread):
    def __init__ (self, _placaBase, _callback):
        self.placaBase = _placaBase
        self.callback = _callback
        Thread.__init__(self)

    def run(self):
        print("Recebe")
        while(True):
            try:
                #self.callback({'id':3, 'codigo':61, 'msg':[randint(0,255)]})
                for i in range(255):
                    self.callback({'id':3, 'codigo':61, 'msg':[i]})
                    sleep(0.2)
                sleep(1)
                for i in range(255,-1,-1):
                    self.callback({'id':3, 'codigo':61, 'msg':[i]})
                    sleep(0.2)
                sleep(1)
                print('----------')
            except Exception as e:
                log("PLB05.3",str(e))
            except KeyboardInterrupt as e:
                self.exit()

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
        try:
            while(self.placaBase.bufferEnvio.empty() == False):
                # print("--------------------------------------")
                #print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                mensagem = self.placaBase.bufferEnvio.get() + '\n'
                print("Thread EnviaMensagens -> " + mensagem)
                # print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                # print("--------------------------------------")
                # while(self.placaBase.portaSerial.isOpen() == False): pass
                # self.placaBase.portaSerial.write(bytes(mensagem, 'UTF-8'))
                sleep(self.placaBase.tempoMinimoEnvio)
            # sleep(0.0001) #evita que o processador vá a 100%
        except Exception as e:
            log("PLB06.0",str(e))
        except KeyboardInterrupt as e:
            self.exit()
