import paho.mqtt.client as mqtt
# import paho.mqtt.publish as publish
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
from aplicacao.models import Leitura, Alarme
from aplicacao.log import log

try:
    config = Mqtt.objects.get()
except Mqtt.DoesNotExist:
    print('erro: Nao existe configuracao na central')
    exit(-1)

def selecionaDados(client):
    # while(True):
    # Seleciona as 50 leituras mais antigas que ainda nao foram enviadas
    leituras = Leitura.objects.filter(sync=False).order_by('createdAt')
    for leitura in leituras:
        message = {
            'valor': leitura.valor,
            'createdAt': str(leitura.createdAt.timestamp())
        }
        try:
            leitura.sync = enviaMensagem(client=client, topic="/central/" + str(config.identificador) +
                                            "/ambiente/" + str(leitura.ambiente.uid) +
                                            "/grandeza/" + str(leitura.grandeza_id) +
                                            "/sensor/" + str(leitura.sensor.uid), message=message)
            leitura.save()
        except Exception as e:
            print(e)
    # Declaracao de Funcao interna

    def enviaAlarme(_client, _alarme):
        """
        Funcao interna para enviar alarmes
        """
        message = {
            'uid': str(_alarme.uid),
            'mensagem': str(_alarme.mensagemAlarme),
            'prioridade': _alarme.prioridadeAlarme,
            'ativo': _alarme.ativo,
            'tempoAtivacao': str(_alarme.tempoAtivacao.timestamp()),
            'tempoInativacao': str(_alarme.tempoInativacao.timestamp()) if _alarme.ativo == False else None
        }
        try:
            return enviaMensagem(client=_client, topic="/central/" + str(config.identificador) +
                                    "/ambiente/" + str(_alarme.ambiente.uid) +
                                    "/grandeza/" + str(_alarme.grandeza_id) +
                                    "/alarme/" +
                                    str(_alarme.codigoAlarme),
                                    message=message)
        except Exception as e:
            print(e)
            return False
        return True
    # Fim de Funcao interna

    # Envia alarmes ativos
    alarmesAtivos = Alarme.objects.filter(syncAtivacao=False).filter(
        ativo=True).order_by('-tempoAtivacao')
    for alarme in alarmesAtivos:
        alarme.syncAtivacao = enviaAlarme(_client=client, _alarme=alarme)
        alarme.save()

    # Envia alarmes inativos que ainda nao foram enviados
    alarmesInativosNaoEnviados = Alarme.objects.filter(
        syncAtivacao=False).filter(ativo=False).order_by('-tempoAtivacao')
    for alarme in alarmesInativosNaoEnviados:
        alarme.syncAtivacao = enviaAlarme(_client=client, _alarme=alarme)
        alarme.save()

    # Envia alarmes inativos
    alarmesInativos = Alarme.objects.filter(syncInativacao=False).filter(
        ativo=False).order_by('-tempoAtivacao')
    for alarme in alarmesInativos:
        alarme.syncInativacao = enviaAlarme(_client=client, _alarme=alarme)
        alarme.save()

def enviaMensagem(client, topic, message):
    try:
        r = client.publish(topic=str(topic),
                            payload=str(message), qos=2, retain=True)
        if(r[0] == mqtt.MQTT_ERR_SUCCESS):
            return True
        elif(r[0] == mqtt.MQTT_ERR_NO_CONN):
            log('MQTT', 'MQTT_ERR_NO_CONN')
            return False
        else:
            log('MQTT', str(r))
            return False
    except Exception as e:
        print("Erro ao enviar uma mensagem")
        if(e.strerror.find('ssl') != -1):
            print(e)
        return False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if(rc == 5):
        print("Invalid user or pass")
        # client.disconnect()
        exit()
        return
    selecionaDados(client)

def on_message(client, userdata, msg):
    try:
        print(msg.topic + ": " + msg.payload.decode('utf-8'))
    except Exception as e:
        print(e)

def on_publish(client, userdata, mid):
    # print(mid)
    # sleep(1)
    # selecionaDados(client)
    pass

def on_disconnect(client, userdata, rc):
    error = True
    while(error):
        try:
            client.reconnect()
            error = False
        except Exception as e:
            if(e.errno == 111):
                print("Conexao recusada")
            else:
                # print(dir(e))
                print(e)
            sleep(1)

client = mqtt.Client(clean_session=True, userdata="None",
                        protocol="MQTTv311", transport="tcp")

client.tls_set(ca_certs=str(config.caFile), certfile=str(config.certFile),
                keyfile=str(config.keyFile), cert_reqs=CERT_REQUIRED, tls_version=PROTOCOL_TLSv1_2)

client.on_connect = on_connect
client.on_message = on_message

client.on_publish = on_publish
client.on_disconnect = on_disconnect

# Extrai o endereço do servidor, excluindo um possível 'http(s)://' e porta
try:
    # http(s)://
    sp = config.servidor.split('//')
    if(len(sp) == 2):
        # tinha 'http(s)://'
        sp = sp[1]

    if(type(sp) == list):
        sp = sp[0]
    # :porta
    sp = sp.split(':')
    if(len(sp) == 2):
        # tinha ':porta'
        sp = sp[0]

    if(type(sp) == list):
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
    sleep(1)
    client.reconnect()
except Exception as e:
    print('Erro: ' + str(e))
    exit(-1)

try:
    while(True):
        selecionaDados(client)
        client.loop(1)
except SSLError as e:
    if(e.reason == 'SSLV3_ALERT_CERTIFICATE_REVOKED'):
        print('O certificado usado foi revogado!')
        exit(-1)
except ConnectionRefusedError:
    print('Falha na conexao com o servidor')
    client.reconnect()
except Exception as e:
    print('Erro no loop: ' + str(e))
except KeyboardInterrupt as e:
    print("\nDesconectando...")
    client.disconnect()
