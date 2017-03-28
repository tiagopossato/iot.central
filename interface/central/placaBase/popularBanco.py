#!/usr/bin/python3
import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.join(__file__ ,"../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.models import Configuracoes, Ambiente, Grandeza, Sensor, SensorGrandeza, SaidaDigital

Configuracoes(
    apiKey = 'AIzaSyCaYACeZvP5sW7MHKA5co7PttejxUxnTTM',
    maxAlarmes = 20,
    portaSerial = '/dev/ttyAMA0',
    taxa = 115200
).save()

Ambiente(nome='Estufa de enraizamento').save()
Ambiente(nome='Estufa de cultivo de mudas').save()

Grandeza(codigo=71, nome='Temperatura', unidade='°C').save()
Grandeza(codigo=72, nome='Umidade do ar', unidade='%uR').save()
Grandeza(codigo=73, nome='Umidade do solo', unidade='%').save()

Sensor(idRede=1, ambiente_id=1, descricao='Sensor de Temperatura e Umidade do ar').save()

SensorGrandeza(grandeza_id=71, sensor_id=1).save()
SensorGrandeza(grandeza_id=72, sensor_id=1).save()

from central.placaIO import newEntradaDigital, newPlacaExpansaoDigital

newPlacaExpansaoDigital(_idRede=3, _descricao="Placa de acionamento das bombas")

newEntradaDigital(_placaExpansaoDigital=3, _numero=0, _triggerAlarme=True, _mensagemAlarme="Contator 1 ligado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Contator 1")
newEntradaDigital(_placaExpansaoDigital=3, _numero=1, _triggerAlarme=True, _mensagemAlarme="Contator 2 ligado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Contator 2")
newEntradaDigital(_placaExpansaoDigital=3, _numero=2, _triggerAlarme=True, _mensagemAlarme="Contator 3 ligado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Contator 3")
newEntradaDigital(_placaExpansaoDigital=3, _numero=3, _triggerAlarme=True, _mensagemAlarme="Contator 4 ligado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Contator 4")
newEntradaDigital(_placaExpansaoDigital=3, _numero=4, _triggerAlarme=True, _mensagemAlarme="Botao de emergencia acionado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Botao de emergencia")


SaidaDigital(numero=1, nome='Bomba de tunel de enraizamento', ativa=True, 
             tempoLigado=20, tempoDesligado=1200, placaExpansaoDigital_id=3, _ambiente_id=1).save()

