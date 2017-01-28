from threading import Thread
import _thread
import serial
import simplejson
from central.views import log
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
            self.bufferEnvio = []
            self.tempoMinimoEnvio = 0.02 #tempo minimo entre uma mensagem e outra
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
            print('placaBase.iniciar(),  ignorando a porta serial')
            self.portaSerial = None
            # self.portaSerial = serial.Serial()
            # self.portaSerial.port = porta
            # self.portaSerial.baudrate = taxa
            # self.portaSerial.parity=serial.PARITY_NONE
            # self.portaSerial.stopbits=serial.STOPBITS_ONE
            # self.portaSerial.bytesize=serial.EIGHTBITS
            # self.portaSerial.timeout=1
            # self.portaSerial.open()


            #Inicia thread para receber as mensagens da placa base
            self._recebe = _RecebeMensagens(self, callback)
            self._recebe.start()
            #inicia thread que envia as mensagens para a placa base
            #self._envia = _EnviaMensagens(self)
            #self._envia.start()
            #inicia a thread que monitora se a placa está online
            #self._monitora = _MonitoraPlacaBase(self)
            #self._monitora.start()

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
            #self.bufferEnvio.insert(0, strComando)
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
            print("placaBase.fechar() ignorando while")
            #while(len(self.bufferEnvio) > 0): sleep(self.tempoMinimoEnvio)
            signal.pthread_kill(self._envia.ident, signal.SIGTERM)
            signal.pthread_kill(self._monitora.ident, signal.SIGTERM)
            signal.pthread_kill(self._recebe.ident, signal.SIGTERM)
            sleep(1)
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
        print('PlacaBase _RecebeMensagens.run() ignorando aqui tbm')
        from random import randint
        while(True):
            for x in range(8):
                self.callback({'id':3,'codigo':61, 'msg':[randint(0,1)]})
                sleep(1)
            pass
        while(True):
            try:
                inMsg = self.placaBase.portaSerial.readline().decode("UTF-8")
                if(len(inMsg) == 0 ):
                    continue
                try:
                    j = simplejson.loads(inMsg)
                    try:
                        if(j['id']==CENTRAL_ID and j['codigo'] == ovcComands['ONLINE']):
                            self.placaBase.isOnline = True
                            continue
                    except Exception as e:
                        log("PLB05.1",str(e) + "["+inMsg+"]")
                        continue
                    self.callback(j)
                except simplejson.scanner.JSONDecodeError as e:
                    #retira a ultima virgula da string
                    #inMsg = inMsg[:len(inMsg) - inMsg[::-1].find(',')-1] + inMsg[len(inMsg) - inMsg[::-1].find(','):]
                    log("PLB05.2",str(e) + "["+inMsg+"]")
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
        print('_EnviaMensagens.run(), fechando')
        return
        while(True):
            try:
                if(len(self.placaBase.bufferEnvio)>0):
                    #print("--------------------------------------")
                    #print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                    mensagem = self.placaBase.bufferEnvio.pop() + '\n'
                    #print("Thread EnviaMensagens -> " + mensagem)
                    #print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                    #print("--------------------------------------")
                    while(self.placaBase.portaSerial.isOpen() == False): pass
                    self.placaBase.portaSerial.write(bytes(mensagem, 'UTF-8'))
                    sleep(self.placaBase.tempoMinimoEnvio)
                sleep(0.0001) #evita que o processador vá a 100%
            except Exception as e:
                log("PLB06.0",str(e))
            except KeyboardInterrupt as e:
                self.exit()

"""
Classe que será chamada via thread para monitorar a comunicação com a placa base
"""
class _MonitoraPlacaBase(Thread):

    def __init__ (self, _placaBase):
        self.placaBase = _placaBase
        self.intervaloVerificacao = 1
        self.tentativas = 2
        self.count = 0
        Thread.__init__(self)

    def run(self):
        print('Thread monitora.run(), saindo!')
        return
        while(True):
            try:
                self.placaBase.isOnline = False
                self.placaBase.enviaComando(CENTRAL_ID, 'IS_ONLINE')
                sleep(self.intervaloVerificacao)
                if(self.count < self.tentativas and self.placaBase.isOnline == False):
                    self.count = self.count + 1
                elif(self.count == self.tentativas and self.placaBase.isOnline == False):
                    self.placaBase.resetPlacaBase()
                    self.count = 0
                elif(self.placaBase.isOnline):
                    self.count = 0
            except Exception as e:
                log("PLB07.1",str(e))
            except KeyboardInterrupt as e:
                self.exit()
