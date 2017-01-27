import datetime
import time
from central.models import PlacaExpansaoDigital, EntradaDigital
from central.views import log, alarmTrigger

def newPlacaExpansaoDigital(_idRede):
    try:
        pli = PlacaExpansaoDigital(idRede=_idRede)
        pli.save()
    except Exception as e:
        log('PLI02',str(e))

def newEntradaDigital(_placaExpansaoDigital, _numero, _codigoAlarme, _nome = ""):
    try:
        entrada = EntradaDigital(numero=_numero, placaExpansaoDigital_id=_placaExpansaoDigital, nome=_nome, codigoAlarme_id = _codigoAlarme)
        entrada.save()
    except Exception as e:
        log('PLI03',str(e))

def updateEntradaDigital(_id, _placaExpansaoDigital=None, _numero=None, _codigoAlarme=-1, _nome=None):
    try:
        entrada = EntradaDigital.objects.get(id = _id)
        try:
            if(_placaExpansaoDigital != None): entrada.placaExpansaoDigital_id = _placaExpansaoDigital
            if(_numero != None): entrada.numero = _numero
            if(_codigoAlarme != -1): entrada.codigoAlarme_id = _codigoAlarme
            if(_codigoAlarme == -1): entrada.codigoAlarme_id = None
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
            print()
            if(int(_estado)==1):
                entrada.estado = True
            else:
                entrada.estado = False
            entrada.sync = False
            entrada.updated_at = datetime.datetime.fromtimestamp(time.time())
            entrada.save()
            if(entrada.codigoAlarme_id != None and entrada.codigoAlarme_id != ''):
                if(_estado == True): alarmTrigger.on(entrada.codigoAlarme_id)
                if(_estado == False): alarmTrigger.off(entrada.codigoAlarme_id)
        return True
    except Exception as e:
        log('PLI05.0',str(e))
    return False
