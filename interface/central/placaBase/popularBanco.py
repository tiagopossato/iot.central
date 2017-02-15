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
    email = 'tiago.possato@yahoo.com.br',
    senha = '123456',
    uidCentral = '-KbztEuoaYejBSl-nyFx',
    maxAlarmes = 20,
    portaSerial = '/dev/ttyAMA0',
    taxa = 115200
).save()

Ambiente(nome='Estufa de enraizamento', uid='-KbztEo7iVuSWveDg3Ge').save()
Ambiente(nome='Estufa de cultivo de flores').save()

Grandeza(codigo=10, nome='Temperatura', unidade='°C').save()
Grandeza(codigo=11, nome='Umidade do ar', unidade='%uR').save()
Grandeza(codigo=12, nome='Umidade do solo', unidade='%').save()

Sensor(idRede=1, ambiente_id=1, descricao='Sensor de Temperatura e Umidade do ar').save()

SensorGrandeza(grandeza_id=10, sensor_id=1).save()
SensorGrandeza(grandeza_id=11, sensor_id=1).save()

from central.alarmes import newAlarmeTipo
from central.placaIO import newEntradaDigital, newPlacaExpansaoDigital

newAlarmeTipo(1,"Disjuntor 1 desarmado", 3)
newAlarmeTipo(2,"Disjuntor 2 desarmado", 3)
newAlarmeTipo(3,"Disjuntor 3 desarmado", 3)
newAlarmeTipo(4,"Disjuntor 4 desarmado", 3)
newAlarmeTipo(5,"Disjuntor 5 desarmado", 3)
newAlarmeTipo(6,"Disjuntor 6 desarmado", 3)
newAlarmeTipo(7,"Disjuntor 7 desarmado", 3)
newAlarmeTipo(8,"Disjuntor 8 desarmado", 3)
newPlacaExpansaoDigital(_idRede=3, _descricao="Placa de acionamento das bombas")
newPlacaExpansaoDigital(_idRede=2)
newEntradaDigital(_placaExpansaoDigital=3, _numero=0, _alarmeTipo = 1, _ambiente_id=1, _nome = "Disjuntor 1")
newEntradaDigital(_placaExpansaoDigital=3, _numero=1, _alarmeTipo = 2, _ambiente_id=1, _nome = "Disjuntor 2")
newEntradaDigital(_placaExpansaoDigital=3, _numero=2, _alarmeTipo = 3, _ambiente_id=1, _nome = "Disjuntor 3")
newEntradaDigital(_placaExpansaoDigital=3, _numero=3, _alarmeTipo = 4, _ambiente_id=1, _nome = "Disjuntor 4")
newEntradaDigital(_placaExpansaoDigital=3, _numero=4, _alarmeTipo = 5, _ambiente_id=1, _nome = "Disjuntor 5")
newEntradaDigital(_placaExpansaoDigital=3, _numero=5, _alarmeTipo = 6, _ambiente_id=1, _nome = "Disjuntor 6")
newEntradaDigital(_placaExpansaoDigital=3, _numero=6, _alarmeTipo = 7, _ambiente_id=1, _nome = "Disjuntor 7")
newEntradaDigital(_placaExpansaoDigital=3, _numero=7, _alarmeTipo = 8, _ambiente_id=1, _nome = "Disjuntor 8")
