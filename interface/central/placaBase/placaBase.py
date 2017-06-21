from threading import Thread
from queue import Queue
import serial
import simplejson
from central.log import log
from central.placaBase.overCAN import tipoGrandeza, grandeza
from time import sleep, time
import signal
import sys
import redis

try:
    import RPi.GPIO as gpio
except RuntimeError as e:
    print(e)
except ImportError as ie:
    print(ie)

CENTRAL_ID = 0


class PlacaBase():
    def iniciar(porta, taxa, callback):
        PlacaBase._isOnline = False
        PlacaBase._bufferEnvio = Queue()
        PlacaBase._bufferRecebimento = Queue()
        PlacaBase._tempoMinimoEnvio = 0.02  # tempo minimo entre uma mensagem e outra
        # Configurando GPIO
        try:
            gpio.setwarnings(False)
            gpio.cleanup()
            gpio.setmode(gpio.BCM)
            # Configurando a direcao do Pino
            gpio.setup(12, gpio.OUT)  # Pino DTR da placaBase
            # Pino de reset da placaBase sempre em HIGH
            gpio.output(12, gpio.HIGH)
        except Exception as e:
            log("PLB01.0", str(e))

        try:
            PlacaBase._portaSerial = serial.Serial()
            PlacaBase._portaSerial.port = porta
            PlacaBase._portaSerial.baudrate = taxa
            PlacaBase._portaSerial.parity = serial.PARITY_NONE
            PlacaBase._portaSerial.stopbits = serial.STOPBITS_ONE
            PlacaBase._portaSerial.bytesize = serial.EIGHTBITS
            PlacaBase._portaSerial.xonxoff = True
            PlacaBase._portaSerial.timeout = None
            PlacaBase._portaSerial.open()
            PlacaBase._callback = callback
        except Exception as e:
            log("PLB01.1", str(e))
            return

        try:
            # Inicia thread para receber as mensagens da placa base
            PlacaBase._thRecebe = _RecebeMensagens()
            PlacaBase._thRecebe.start()
            # Inicia thread para tratar as mensagens recebidas da placa base
            PlacaBase._thCallback = _CallbackRecebe()
            PlacaBase._thCallback.start()
            # inicia thread que envia as mensagens para a placa base
            PlacaBase._thEnvia = _EnviaMensagens()
            PlacaBase._thEnvia.start()
            # inicia a thread que monitora se a placa está online
            PlacaBase._thMonitora = _MonitoraPlacaBase()
            PlacaBase._thMonitora.start()

            PlacaBase.initDB()
            p = PlacaBase._db.pubsub()
            p.subscribe(**{'msg': PlacaBase._ipc})
            thread = p.run_in_thread(sleep_time=0.01)

        except Exception as e:
            log("PLB01.2", str(e))

    def _ipc(message):
        PlacaBase._bufferEnvio.put(message['data'].decode("UTF-8"))
        # verifica se a thread está ativa
        if(PlacaBase._thEnvia.isAlive() == False):
            PlacaBase._thEnvia.run()

    def initDB():
        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            PlacaBase._db = redis.Redis(connection_pool=pool)
        except Exception as e:
            print(str(e))

    def enviaComando(idRede, tipoGrandeza, grandeza, valor=''):
        try:
            try:
                PlacaBase._db
            except AttributeError:
                PlacaBase.initDB()
            strComando = '['
            strComando += str(int(idRede))
            strComando += '/'
            strComando += str(tipoGrandeza_CAN[tipoGrandeza])
            strComando += '/'
            strComando += str(grandeza_CAN[tipoGrandeza])
            strComando += '/'
            strComando += str(msg)
            strComando += ']'
            #log("PLB02.0","O parâmetro msg deve ser uma única string ou uma tupla de strings")
#            print(strComando)
            PlacaBase._db.publish('msg', strComando)
            # PlacaBase._bufferEnvio.put(strComando)
            # verifica se a thread está ativa
            # if(PlacaBase._thEnvia.isAlive() == False):
            #     PlacaBase._thEnvia.run()
        except Exception as e:
            log("PLB02.1", str(e))

    def resetPlacaBase():
        try:
            gpio.output(12, gpio.LOW)
            sleep(0.5)
            gpio.output(12, gpio.HIGH)
            log("PLB03.0", "Resetando placaBase")
        except Exception as e:
            log("PLB03.1", str(e))

    def fechar():
        try:
            print("Aguardando esvaziar buffer de envio")
            while(PlacaBase._bufferEnvio.empty() == False):
                tam = PlacaBase._bufferEnvio.qsize()
                sleep(PlacaBase._tempoMinimoEnvio * 5)
                # caso nenhuma mensagem foi enviada assume-se que tem algum erro
                if(tam == PlacaBase._bufferEnvio.qsize()):
                    break

            print("Aguardando threads terminarem")

            try:
                signal.pthread_kill(PlacaBase._thEnvia.ident, signal.SIGKILL)
                PlacaBase._thEnvia.join()
            except Exception as e:
                print("_thEnvia")
                print(e)

            try:
                signal.pthread_kill(
                    PlacaBase._thMonitora.ident, signal.SIGKILL)
                PlacaBase._thMonitora.join()
            except Exception as e:
                print("_thMonitora")
                print(e)

            try:
                signal.pthread_kill(PlacaBase._thRecebe.ident, signal.SIGKILL)
                PlacaBase._thRecebe.join()
            except Exception as e:
                print("_thRecebe")
                print(e)

            try:
                signal.pthread_kill(
                    PlacaBase._thCallback.ident, signal.SIGKILL)
                PlacaBase._thCallback.join()
            except Exception as e:
                print("_thCallback")
                print(e)

            PlacaBase._portaSerial.close()

        except Exception as e:
            print("Fechando placa base")
            print(e)
            sys.exit(0)


"""
Classe que será chamada via thread para receber as mensagens da porta serial
"""


class _RecebeMensagens(Thread):
    def __init__(self):
        Thread.__init__(self, name="_RecebeMensagens")

    def run(self):
        try:
            print(Thread.getName(self))
            while(True):
                try:
                    inMsg = PlacaBase._portaSerial.readline()
                except Exception as e:
                    log("PLB04.0", str(e))
                    continue

                try:
                    inMsg = inMsg.decode("UTF-8")
                    print(inMsg)
                    if(len(inMsg) == 0):
                        continue
                except Exception as e:
                    log("PLB04.1", str(e))
                    continue

                try:
                    # extrai as informações da URI e transforma em um objeto
                    # retira a mensagem de dentro das chaves [mensagem]
                    parcial = inMsg[inMsg.index(
                        '[') + 1:inMsg.index(']')].split("/")
                    msg = {}
                    try:
                        msg['id'] = parcial[0]
                        msg['tipoGrandeza'] = parcial[1]
                        msg['grandeza'] = parcial[2]
                        msg['valor'] = parcial[3]
                    except Exception as e:
                        log("PLB04.2", str(e) + "[" + msg + "]")

                    try:
                        if(msg['id'] == CENTRAL_ID and msg['tipoGrandeza'] == tipoGrandeza['especial']
                                and msg['grandeza'] == grandeza['online']):
                            PlacaBase._isOnline = True
                            continue
                    except Exception as e:
                        log("PLB04.2", str(e) + "[" + msg + "]")
                        continue

                    PlacaBase._bufferRecebimento.put(msg)
                    # verifica se a thread está ativa
                    if(PlacaBase._thCallback.isAlive() == False):
                        PlacaBase._thCallback.run()

                except ValueError as e:
                    log("PLB04.3", str(e) + "[" + inMsg + "]")
                    continue
                except Exception as e:
                    log("PLB04.4", str(e))
                    continue
        except KeyboardInterrupt as e:
            return


"""
Thread para processar as mensagens recebidas
"""


class _CallbackRecebe(Thread):
    def __init__(self):
        Thread.__init__(self, name="_CallbackRecebe")
        print(Thread.getName(self))

    def run(self):
        try:
            while(PlacaBase._bufferRecebimento.empty() == False):
                PlacaBase._callback(PlacaBase._bufferRecebimento.get())
        except Exception as e:
            log("PLB05.0", str(e))
        except KeyboardInterrupt as e:
            self.exit()


"""
Classe que será chamada via thread para enviar as mensagens para porta serial
Esta classe envia as mensagens do _bufferEnvio do objeto placaBase respeitando
o tempo mínimo da placaBase
"""


class _EnviaMensagens(Thread):
    def __init__(self):
        Thread.__init__(self, name="_EnviaMensagens")
        print(Thread.getName(self))

    def run(self):
        try:
            # print(Thread.getName(self))
            while(PlacaBase._bufferEnvio.empty() == False):
                # print("--------------------------------------")
                #print("PlacaBase._bufferEnvio: " + str(PlacaBase._bufferEnvio))
                mensagem = PlacaBase._bufferEnvio.get() + '\n'
                # print("Thread EnviaMensagens -> " + mensagem)
                # print("PlacaBase._bufferEnvio: " + str(PlacaBase._bufferEnvio))
                # print("--------------------------------------")
                while(PlacaBase._portaSerial.isOpen() == False):
                    pass
                PlacaBase._portaSerial.write(bytes(mensagem, 'UTF-8'))
                PlacaBase._portaSerial.flushOutput()
                sleep(PlacaBase._tempoMinimoEnvio)
            # sleep(0.0001) #evita que o processador vá a 100%
        except Exception as e:
            log("PLB06.0", str(e))
        except KeyboardInterrupt as e:
            return


"""
Classe que será chamada via thread para monitorar a comunicação com a placa base
"""


class _MonitoraPlacaBase(Thread):

    def __init__(self):
        self._intervaloVerificacao = 2
        self._tentativas = 5
        self._count = 0
        Thread.__init__(self, name="_MonitoraPlacaBase")

    def run(self):
        print(Thread.getName(self))
        while(True):
            try:
                PlacaBase._isOnline = False
                PlacaBase.enviaComando(idRede=self.CENTRAL_ID,
                                       tipoGrandeza='ESPECIAL', grandeza='ONLINE', valor=True)

                sleep(self._intervaloVerificacao)
                if(self._count < self._tentativas and PlacaBase._isOnline == False):
                    self._count = self._count + 1
                elif(self._count == self._tentativas and PlacaBase._isOnline == False):
                    PlacaBase.resetPlacaBase()
                    self._count = 0
                elif(PlacaBase._isOnline):
                    self._count = 0
            except Exception as e:
                log("PLB07.0", str(e))
            except KeyboardInterrupt as e:
                self.exit()
