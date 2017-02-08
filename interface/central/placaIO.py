import datetime
import time
from central.models import PlacaExpansaoDigital, EntradaDigital
from central.log import log
from central.alarmes import AlarmTrigger

alarmTrigger = AlarmTrigger()

def newPlacaExpansaoDigital(_idRede):
    try:
        pli = PlacaExpansaoDigital(idRede=_idRede)
        pli.save()
    except Exception as e:
        log('PLI02',str(e))

def newEntradaDigital(_placaExpansaoDigital, _numero, _alarmeTipo, _ambiente_id, _nome = ""):
    try:
        entrada = EntradaDigital(numero=_numero, 
            placaExpansaoDigital_id=_placaExpansaoDigital, 
            ambiente_id = _ambiente_id,
            nome=_nome, 
            alarmeTipo_id = _alarmeTipo)
        entrada.save()
    except Exception as e:
        log('PLI03',str(e))

def updateEntradaDigital(_id, _placaExpansaoDigital=None, _numero=None, _alarmeTipo=-1, _nome=None):
    try:
        entrada = EntradaDigital.objects.get(id = _id)
        try:
            if(_placaExpansaoDigital != None): entrada.placaExpansaoDigital_id = _placaExpansaoDigital
            if(_numero != None): entrada.numero = _numero
            if(_alarmeTipo != -1): entrada.alarmeTipo.id = _alarmeTipo
            if(_alarmeTipo == -1): entrada.alarmeTipo.id = None
            if(_nome != None): entrada.nome = _nome
            entrada.updated_at = datetime.datetime.fromtimestamp(time.time())
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
        entrada = EntradaDigital.objects.get(\
            placaExpansaoDigital_id = _codigoPlacaExpansaoDigital,\
            numero = _numero)
        if(int(entrada.estado) != int(_estado)):
            print("Update no "+entrada.nome+" -> "+str(_estado))
            entrada.estado = bool(int(_estado))
            entrada.sync = False
            entrada.updated_at = datetime.datetime.fromtimestamp(time.time())
            entrada.save()
            if(entrada.alarmeTipo.id != None and entrada.alarmeTipo.id != ''):
                if(int(_estado) == True): alarmTrigger.on(_alarmeTipo_id=entrada.alarmeTipo.id, _ambiente=entrada.ambiente.id)
                if(int(_estado) == False): alarmTrigger.off(_alarmeTipo_id=entrada.alarmeTipo.id)
        return True
    except Exception as e:
        log('PLI05.0',str(e))
    return False
