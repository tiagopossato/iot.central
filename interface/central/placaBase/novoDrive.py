import socket
import sys
from central.log import log
from central.placaBase.overCAN import tipoGrandeza_CAN, grandeza_CAN, configuracoes_CAN

server_address = '/tmp/placaBase.socket'

class PlacaBase():
    def enviaComando(idRede, tipoGrandeza, grandeza, valor=''):
        try:
            strComando = '['
            strComando += str(int(idRede))
            strComando += '/'
            strComando += str(tipoGrandeza_CAN[tipoGrandeza])
            strComando += '/'
            try:
                strComando += str(grandeza_CAN[grandeza])
            except KeyError:
                try:
                    strComando += str(configuracoes_CAN[grandeza])
                except KeyError:
                    strComando += str(grandeza)

            strComando += '/'
            strComando += str(valor)
            strComando += ']'
            print("enviaComando: " + strComando)
            #envia para o drive da placa base
            try:
                # Cria o socket
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                #conecta no endereço
                sock.connect(server_address)
                #envia os dados
                sock.send(bytes(saida, 'UTF-8'))
            except socket.error as e:
                log("NVD01.0", str(e))
            except OSError as e:
                log("NVD01.1", str(e))
            finally:
                sock.close()
        except Exception as e:
            print(e)
            log("NVD01.2", str(e))