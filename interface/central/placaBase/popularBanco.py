#!/usr/bin/python3
import os
import sys
import django

sys.path.insert(0, os.path.abspath('../../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.models import Configuracoes, Ambiente, Grandeza, Sensor, SensorGrandeza

Configuracoes(
    apiKey = 'AIzaSyCaYACeZvP5sW7MHKA5co7PttejxUxnTTM',
    authDomain = 'testes-apisensores.firebaseapp.com',
    databaseURL = 'https://testes-apiSensores.firebaseio.com',
    storageBucket = 'testes-apiSensores.appspot.com',
    uidCentral = '-KbztEuoaYejBSl-nyFx',
    maxAlarmes = 20,
    portaSerial = '/dev/ttyAMA0',
    taxa = 115200
).save()

Ambiente(nome='Estufa de enraizamento').save()
Ambiente(nome='Estufa de cultivo de flores').save()

Grandeza(codigo=71, nome='Temperatura', unidade='°C').save()
Grandeza(codigo=72, nome='Umidade do ar', unidade='%uR').save()
Grandeza(codigo=73, nome='Umidade do solo', unidade='%').save()

Sensor(idRede=1, ambiente_id=1, descricao='Sensor de Temperatura e Umidade do ar').save()

SensorGrandeza(grandeza_id=71, sensor_id=1).save()
SensorGrandeza(grandeza_id=72, sensor_id=1).save()

from central.placaIO import newEntradaDigital, newPlacaExpansaoDigital

newPlacaExpansaoDigital(_idRede=3, _descricao="Placa de acionamento das bombas")
newPlacaExpansaoDigital(_idRede=2)
newEntradaDigital(_placaExpansaoDigital=3, _numero=0, _triggerAlarme=True, _mensagemAlarme="Disjuntor 1 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 1")
newEntradaDigital(_placaExpansaoDigital=3, _numero=1, _triggerAlarme=True, _mensagemAlarme="Disjuntor 2 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 2")
newEntradaDigital(_placaExpansaoDigital=3, _numero=2, _triggerAlarme=True, _mensagemAlarme="Disjuntor 3 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 3")
newEntradaDigital(_placaExpansaoDigital=3, _numero=3, _triggerAlarme=True, _mensagemAlarme="Disjuntor 4 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 4")
newEntradaDigital(_placaExpansaoDigital=3, _numero=4, _triggerAlarme=True, _mensagemAlarme="Disjuntor 5 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 5")
newEntradaDigital(_placaExpansaoDigital=3, _numero=5, _triggerAlarme=True, _mensagemAlarme="Disjuntor 6 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 6")
newEntradaDigital(_placaExpansaoDigital=3, _numero=6, _triggerAlarme=True, _mensagemAlarme="Disjuntor 7 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 7")
newEntradaDigital(_placaExpansaoDigital=3, _numero=7, _triggerAlarme=True, _mensagemAlarme="Disjuntor 8 desarmado", _prioridadeAlarme=3, _ambiente_id=1, _nome = "Disjuntor 8")
