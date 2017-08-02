import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from ssl import PROTOCOL_TLSv1_2, CERT_REQUIRED, SSLError
from time import sleep, time
import random

# Configurações para usar os models do django
import os
import sys
import django
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "central.settings"
django.setup()

from comunicacao.models import Mqtt
try:
    config = Mqtt.objects.get()
except Mqtt.DoesNotExist:
    print('erro: Nao existe configuracao na central')
    exit(-1)


def enviaMensagemVelho(client):
    message = {
        "ambiente": "8cb54a24-a51e-4ac8-8113-12f12c9596da",
        "sensor": 1,
        "createdAt": 1496918500,
        "grandeza": 3303,
        "valor": random.uniform(15.5, 31.9)
    }
    client.publish("/central/" + str(config.identificador) +
                   "/ambiente/b8b35b7f79c447748ac456e08de34a50/grandeza/3303/sensor/4", payload=str(message), qos=0, retain=True)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if(rc == 5):
        print("Invalid user or pass")
        # client.disconnect()
        exit()
        return
    enviaMensagemVelho(client)

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # print(dir(msg))
    try:
        print(msg.topic + ": " + msg.payload.decode('utf-8'))
    except Exception as e:
        print(e)


def on_publish(client, userdata, mid):
    # client.disconnect()
    sleep(5)
    enviaMensagemVelho(client)


def on_disconnect(client, userdata, rc):
    client.reconnect()


client = mqtt.Client(clean_session=True, userdata="None",
                     protocol="MQTTv311", transport="tcp")

client.tls_set(ca_certs=config.caFile, certfile=config.certFile,
               keyfile=config.keyFile, cert_reqs=CERT_REQUIRED, tls_version=PROTOCOL_TLSv1_2)

client.on_connect = on_connect
#client.on_message = on_message

client.on_publish = on_publish
client.on_disconnect = on_disconnect
# Extrai o endereço do servidor, excluindo um possível 'http(s)://' e porta
try:
    # http(s)://
    sp = config.servidor.split('//')
    if(len(sp) == 2):
        # tinha 'http(s)://'
        sp = sp[1]

    if(type(sp)==list):
        sp = sp[0]
    # :porta
    sp = sp.split(':')
    if(len(sp) == 2):
        # tinha ':porta'
        sp = sp[0]

    if(type(sp)==list):
        sp = sp[0]
    
    urlServidor = sp
except IndexError as e:
    print(e)
    exit(-1)

try:
    client.connect(urlServidor, 8883, 60)
except SSLError as e:
    if(e.reason == 'SSLV3_ALERT_CERTIFICATE_REVOKED'):
        print('O certificado usado foi revogado!')
        exit(-1)
except ConnectionRefusedError:
    print('Falha na conexao com o servidor')
    exit(-1)
except Exception as e:
    print('Erro: ' + str(e))
    exit(-1)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

try:
    client.loop_forever()
except SSLError as e:
    if(e.reason == 'SSLV3_ALERT_CERTIFICATE_REVOKED'):
        print('O certificado usado foi revogado!')
        exit(-1)
except ConnectionRefusedError:
    print('Falha na conexao com o servidor')
    exit(-1)
except Exception as e:
    print('Erro no loop: ' + str(e))
except KeyboardInterrupt as e:
    print("\nDesconectando...")
    client.disconnect()
