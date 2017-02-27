import datetime
import time
from central.models import Sensor, Leitura
from central.log import log
from django.core.exceptions import ObjectDoesNotExist
from central.alarmeAnalogico import triggerAlarmeAnalogico

def newLeitura(_idRedeSensor,_grandeza, _valor):
    # sensor = Sensor.objects.get(idRede=_idRedeSensor, grandezas__codigo=_grandeza)
    try:
        sensor = Sensor.objects.get(idRede=_idRedeSensor)
    except ObjectDoesNotExist as e:
        log('SEN01.0','Nova leitura. O Sensor ' + str(_idRedeSensor) + ' não está cadastrado')
        return False

    try:
        grandeza = sensor.grandezas.get(sensorgrandeza__grandeza=_grandeza)
    except ObjectDoesNotExist as e:
        log('SEN01.1','Nova leitura. O Sensor ' + str(_idRedeSensor) + ', não possui a Grandeza ' + 
            str(_grandeza) + ' cadastrada.')
        return False
    
    try:
        _valor = format(_valor, '.2f')
        l = Leitura(valor=_valor, sensor=sensor, grandeza=grandeza, ambiente=sensor.ambiente)
        l.save()
        print(str(sensor) + ': '+ str(_valor) + ' ' + str(grandeza) + '[' + str(l.created_at) + ']')
        triggerAlarmeAnalogico(_grandeza=grandeza, _ambiente=sensor.ambiente)
    except Exception as e:
        log('SEN01.2','Nova leitura: ' + str(e))
        return False

    return True