from django.shortcuts import render

import datetime
import time
from central.util import salvaArquivo
from central.models import Log, AlarmeTipo, Alarme

"""
Salva um log na tabela de logs
"""
def log(_tipo, _mensagem):
    try:
        lg = Log(mensagem=_mensagem, tipo = _tipo)
        lg.save()
        print('['+ datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')\
    + '] [' + _tipo + '] [' + _mensagem + ']')
    except Exception as e:
        salvaArquivo('LOG01', str(e))
        salvaArquivo(_tipo, _mensagem)

"""
Cria um novo tipo de alarme
"""
def newAlarmeTipo(_codigo, _mensagem, _prioridade):
    try:
        at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
        at.save()
    except Exception as e:
        log('ALM01',str(e))

class alarmTrigger():
    def on(codigo):
        try:
            #verifica se o codigo do alarme já está ativo
            at = Alarme.objects.get(codigoAlarme_id = codigo, ativo = True)
            #O alarme já está ativo
            log('ALM02','O alarme já está ativo')
            return True
        except Alarme.DoesNotExist:
            at = None
        except Exception as e:
            print(e)
            log('ALM03',str(e))
            return False
        #Insere um novo alarme na tabela
        try:
            a = Alarme(codigoAlarme_id=codigo, ativo=True, syncAtivacao=False, tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
            a.save()
            return True
        except Exception as e:
            log('ALM04',str(e))
            return False

    def off(codigo):
        try:
            #verifica se o codigo do alarme está ativo
            alm = Alarme.objects.get(codigoAlarme = codigo, ativo = True)
            #O alarme já está ativo, desativa
            try:
                #Altera alarme na tabela
                alm.tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                alm.ativo = False
                alm.syncInativacao = False
                alm.save()
                #_SincronizaAlarmes(_completo=False).start()
                return True
            except Exception as e:
                log('ALM06',str(e))
                return False
        except Alarme.DoesNotExist:
            #O alarme não está ativo
            return False
        except Exception as e:
            log('ALM07',str(e))
            return False
