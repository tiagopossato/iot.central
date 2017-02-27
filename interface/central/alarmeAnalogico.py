from central.log import log
from central.alarmeTrigger import alarmeTrigger
from central.models import AlarmeAnalogico


def newAlarmeAnalogico(_mensagemAlarme, _prioridadeAlarme,
                        _valorAlarmeOn, _valorAlarmeOff,
                        _ambiente_id, _grandeza_id):
    try:
        AlarmeAnalogico(mensagemAlarme = _mensagemAlarme, prioridadeAlarme = _prioridadeAlarme,
                            valorAlarmeOn = _valorAlarmeOn, valorAlarmeOff=_valorAlarmeOff,
                            ambiente_id = _ambiente_id, grandeza_id = _grandeza_id
                        ).save()
    except Exception as e:
        log('AAN01',str(e))

def updateAlarmeAnalogico(_codigoAlarme, _mensagemAlarme, _prioridadeAlarme,
                        _valorAlarmeOn, _valorAlarmeOff,
                        _ambiente_id, _grandeza_id):
    try:
        alm = EntradaDigital.objects.get(codigoAlarme = _codigoAlarme)

        alm.mensagemAlarme = _mensagemAlarme
        alm.prioridadeAlarme = _prioridadeAlarme
        alm.valorAlarmeOn = _valorAlarmeOn
        alm.valorAlarmeOff=_valorAlarmeOff
        alm.ambiente_id = _ambiente_id
        alm.grandeza_id = _grandeza_id
        alm.save()
    except Exception as e:
        log('AAN02',str(e))