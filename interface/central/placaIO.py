import datetime
import time
from central.models import PlacaExpansaoDigital, EntradaDigital
from central.log import log
from central.alarmeTrigger import alarmeTrigger

def newPlacaExpansaoDigital(_idRede,_descricao=""):
    try:
        PlacaExpansaoDigital(idRede=_idRede, descricao=_descricao).save()
    except Exception as e:
        log('PLI02',str(e))

def newEntradaDigital(_placaExpansaoDigital,
                     _numero, _triggerAlarme, 
                     _mensagemAlarme, _prioridadeAlarme,
                     _ambiente_id, _nome = ""):
    try:
        EntradaDigital(numero=_numero, 
            placaExpansaoDigital_id=_placaExpansaoDigital, 
            ambiente_id = _ambiente_id,
            nome=_nome, triggerAlarme = _triggerAlarme,
            mensagemAlarme = _mensagemAlarme,
            prioridadeAlarme = _prioridadeAlarme
        ).save()
    except Exception as e:
        log('PLI03',str(e))

def updateEntradaDigital(_id, _placaExpansaoDigital=None, 
                        _numero=None,_nome=None,
                        _mensagemAlarme=None,_prioridadeAlarme=None):
    try:
        entrada = EntradaDigital.objects.get(id = _id)
        try:
            if(_placaExpansaoDigital != None): entrada.placaExpansaoDigital_id = _placaExpansaoDigital
            if(_numero != None): entrada.numero = _numero
            if(_nome != None): entrada.nome = _nome

            if(_mensagemAlarme != None and _prioridadeAlarme != None):
                entrada.mensagemAlarme = _mensagemAlarme
                entrada.prioridadeAlarme = _prioridadeAlarme          

            entrada.updatedAt = datetime.datetime.fromtimestamp(time.time())
            entrada.save()
            return True
        except Exception as e:
            log('PLI04.0',str(e))
            return False
    except Exception as e:
        log('PLI04.1',str(e))
    return False


def alteraEstadoEntrada(_codigoPlacaExpansaoDigital, _numero, _estado):
    try:
        entrada = EntradaDigital.objects.get(
            placaExpansaoDigital_id = _codigoPlacaExpansaoDigital,
            numero = _numero
        )
        if(int(entrada.estado) != int(_estado)):
            print("Update no "+entrada.nome+" -> "+str(_estado))
            entrada.estado = bool(int(_estado))
            entrada.sync = False
            entrada.updatedAt = datetime.datetime.fromtimestamp(time.time())
            entrada.save()

        if(int(_estado) == entrada.triggerAlarme):
            alarmeTrigger.on(
                _codigoAlarme = entrada.codigoAlarme, 
                _ambiente = entrada.ambiente.id,
                _mensagemAlarme = entrada.mensagemAlarme,
                _prioridadeAlarme = entrada.prioridadeAlarme
                )
        if(int(_estado) != entrada.triggerAlarme):
            alarmeTrigger.off(_codigoAlarme=entrada.codigoAlarme)

        return True
    except Exception as e:
        log('PLI05.0',str(e))
    return False
