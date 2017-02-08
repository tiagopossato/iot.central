from threading import Thread
from queue import Queue
import serial
import simplejson
from central.log import log
from central.placaBase.overCAN import ovcComands
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
            self.bufferRecebimento = Queue()
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
            self.portaSerial = serial.Serial()
            self.portaSerial.port = porta
            self.portaSerial.baudrate = taxa
            self.portaSerial.parity=serial.PARITY_NONE
            self.portaSerial.stopbits=serial.STOPBITS_ONE
            self.portaSerial.bytesize=serial.EIGHTBITS
            self.portaSerial.xonxoff = True
            self.portaSerial.timeout=None
            self.portaSerial.open()
            self.callback = callback

            #Inicia thread para receber as mensagens da placa base
            self._thRecebe = _RecebeMensagens(self)
            self._thRecebe.start()
            #Inicia thread para tratar as mensagens recebidas da placa base
            self._thCallback = _CallbackRecebe(self)
            self._thCallback.start()
            #inicia thread que envia as mensagens para a placa base
            self._thEnvia = _EnviaMensagens(self)
            self._thEnvia.start()
            #inicia a thread que monitora se a placa está online
            self._thMonitora = _MonitoraPlacaBase(self)
            self._thMonitora.start()

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
            if(self._thEnvia.isAlive() == False):
                self._thEnvia.run()
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
            print("Aguardando threads terminarem")
            
            try:
                signal.pthread_kill(self._thEnvia.ident, signal.SIGKILL)
                self._thEnvia.join()
            except Exception as e:
                print("_thEnvia")
                print(e)               
            
            try:
                signal.pthread_kill(self._thMonitora.ident, signal.SIGKILL)
                self._thMonitora.join() 
            except Exception as e:
                print("_thMonitora")
                print(e)

            try:
                signal.pthread_kill(self._thRecebe.ident, signal.SIGKILL)
                self._thRecebe.join()
            except Exception as e:
                print("_thRecebe")
                print(e)

            try:
                signal.pthread_kill(self._thCallback.ident, signal.SIGKILL)
                self._thCallback.join()
            except Exception as e:
                print("_thCallback")
                print(e)

            self.portaSerial.close()

        except Exception as e:
            print("Fechando placa base")
            print(e)
            sys.exit(0)

"""
Classe que será chamada via thread para receber as mensagens da porta serial
"""
class _RecebeMensagens(Thread):
    def __init__ (self, _placaBase):
        self.placaBase = _placaBase
        Thread.__init__(self, name="_RecebeMensagens")

    def run(self):
        try:
            print(Thread.getName(self))
            while(True):
                try:
                    # inMsg = ''
                    # while(True):
                    #     print(self.placaBase.portaSerial.read(1).decode('utf-8'))
                    #     if(data == '\n'):
                    #         break
                    #     if(data):
                    #         inMsg += data.decode()
                    # #inMsg = self.placaBase.portaSerial.readline().decode("UTF-8")
                    # print(str(inMsg))
                    inMsg = self.placaBase.portaSerial.readline()
                    inMsg = inMsg.decode("UTF-8")
                    # print(inMsg)
                    if(len(inMsg) == 0 ):
                        continue
                except Exception as e:
                    log("PLB05.0",str(e))
                
                try:
                    j = simplejson.loads(inMsg)
                    try:
                        if(j['id']==CENTRAL_ID and j['codigo'] == ovcComands['ONLINE']):
                            self.placaBase.isOnline = True
                            continue
                    except Exception as e:
                        log("PLB05.1",str(e) + "["+inMsg+"]")
                        continue
                    
                    self.placaBase.bufferRecebimento.put(j)
                    #verifica se a thread está ativa
                    if(self.placaBase._thCallback.isAlive() == False):
                        self.placaBase._thCallback.run()

                except simplejson.scanner.JSONDecodeError as e:
                    log("PLB05.2",str(e) + "["+inMsg+"]")
                except Exception as e:
                    log("PLB05.3",str(e))
        except KeyboardInterrupt as e:
            self.exit()

"""
Thread para processar as mensagens recebidas
"""
class _CallbackRecebe(Thread):
    def __init__ (self, _placaBase):
        self.placaBase = _placaBase
        Thread.__init__(self, name="_CallbackRecebe")
        print(Thread.getName(self))

    def run(self):
        try:            
            while(self.placaBase.bufferRecebimento.empty() == False):
                self.placaBase.callback(self.placaBase.bufferRecebimento.get())
        except Exception as e:
            log("PLB06.0",str(e))
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
        Thread.__init__(self, name="_EnviaMensagens")
        print(Thread.getName(self))

    def run(self):
        try:
            #print(Thread.getName(self))
            while(self.placaBase.bufferEnvio.empty() == False):
                # print("--------------------------------------")
                #print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                mensagem = self.placaBase.bufferEnvio.get() + '\n'
                # print("Thread EnviaMensagens -> " + mensagem)
                # print("self.placaBase.bufferEnvio: " + str(self.placaBase.bufferEnvio))
                # print("--------------------------------------")
                while(self.placaBase.portaSerial.isOpen() == False): pass
                self.placaBase.portaSerial.write(bytes(mensagem, 'UTF-8'))
                self.placaBase.portaSerial.flushOutput()
                sleep(self.placaBase.tempoMinimoEnvio)
            # sleep(0.0001) #evita que o processador vá a 100%
        except Exception as e:
            log("PLB07.0",str(e))
        except KeyboardInterrupt as e:
            return

"""
Classe que será chamada via thread para monitorar a comunicação com a placa base
"""
class _MonitoraPlacaBase(Thread):

    def __init__ (self, _placaBase):
        self.placaBase = _placaBase
        self.intervaloVerificacao = 2
        self.tentativas = 5
        self.count = 0
        Thread.__init__(self, name="_MonitoraPlacaBase")      

    def run(self):
        print(Thread.getName(self))
        while(True):
            try:
                self.placaBase.isOnline = False
                #self.placaBase.enviaComando(CENTRAL_ID, 'IS_ONLINE')
                sleep(self.intervaloVerificacao)
                if(self.count < self.tentativas and self.placaBase.isOnline == False):
                    self.count = self.count + 1
                elif(self.count == self.tentativas and self.placaBase.isOnline == False):
                    self.placaBase.resetPlacaBase()
                    self.count = 0
                elif(self.placaBase.isOnline):
                    self.count = 0
            except Exception as e:
                log("PLB08.0",str(e))
            except KeyboardInterrupt as e:
                self.exit()
