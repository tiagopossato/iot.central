import datetime
import time
from central.models import Sensor, Leitura
from central.log import log
from django.core.exceptions import ObjectDoesNotExist
from central.alarmeAnalogico import triggerAlarmeAnalogico
from central.models import Configuracoes
from central.firebase.conectaFirebase import ConectaFirebase

def novoSensorFirebase(sensor):
    try:
        ConectaFirebase()
        user = ConectaFirebase.getUser()
        db = ConectaFirebase.db
        dados = {}
        dados['idRede'] = sensor.idRede
        dados['descricao'] = sensor.descricao
        dados['createdAt'] = sensor.createdAt.timestamp()
        dados['intervaloAtualizacao'] = sensor.intervaloAtualizacao
        dados['ambiente'] = sensor.ambiente.uid
        dados['central'] = Configuracoes.objects.get().uidCentral
        print(dados)
        sen = db.child("sensores").push(dados, user['idToken'])
        db.child("ambientes").child(sensor.ambiente.uid).child('sensores').child(sen['name']).set(True, user['idToken'])
        sensor.uid = sen['name']
        return sensor
    except Exception as e:   
        print(e.strerror)
        return False

def alteraSensorFirebase(sensor):
    try:
        dados = {}
        dados['idRede'] = sensor.idRede
        dados['descricao'] = sensor.descricao
        dados['createdAt'] = sensor.createdAt.timestamp()
        dados['intervaloAtualizacao'] = sensor.intervaloAtualizacao
        dados['ambiente'] = sensor.ambiente.uid
        dados['central'] = Configuracoes.objects.get().uidCentral
        dados['grandezas'] = {}
        for g in sensor.sensorgrandeza_set.values():
            dados['grandezas'][g['grandeza_id']] = True

        print(dados)
        ConectaFirebase()
        user = ConectaFirebase.getUser()
        db = ConectaFirebase.db
        amb = db.child("sensores").child(sensor.uid).set(dados, user['idToken'])
        #verifica se foi alterado de ambiente
        if(sensor.get_previous_by_updatedAt().uid != sensor.ambiente.uid):
            #altera o relacionamento antigo
            db.child("ambientes").child(sensor.get_previous_by_updatedAt().ambiente.uid).child('sensores').child(sensor.uid).set(False, user['idToken'])
            # inclui o novo relacionamento
            db.child("ambientes").child(sensor.ambiente.uid).child('sensores').child(sensor.uid).set(True, user['idToken'])
        return sensor      
    except Exception as e:
        print('alteraSensorFirebase: ' + str(e))
        return False


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
        print(str(sensor) + ': '+ str(_valor) + ' ' + str(grandeza) + '[' + str(l.createdAt) + ']')
        triggerAlarmeAnalogico(_grandeza=grandeza, _ambiente=sensor.ambiente)
    except Exception as e:
        log('SEN01.2','Nova leitura: ' + str(e))
        return False

    return True
    