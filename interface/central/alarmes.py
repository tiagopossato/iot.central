import datetime
import time
from threading import Thread

from central.placaBase.configuracao import config
from central.models import Alarme, Ambiente
from central.log import log

from central.firebase.alarmesFirebase import SincronizaAlarmes
# from central.servidor.alarmesServidor import SincronizaAlarmes

"""
Cria um novo tipo de alarme
"""
# def newAlarmeTipo(_codigo, _mensagem, _prioridade):
#     try:
#         at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
#         at.save()
#     except Exception as e:
#         log('ALM01',str(e))

class alarmTrigger():

    def on(_codigoAlarme, _mensagemAlarme, _prioridadeAlarme, _ambiente):
        try:
            #verifica se o codigo do alarme já está ativo
            alm = Alarme.objects.\
                filter(codigoAlarme = _codigoAlarme, ativo = True)\
                .order_by('id').all()
        except Exception as e:
            log('ALM02.0',str(e))
            return False
        
        try:
            if(len(alm)==1):
                #O alarme já está ativo
                # log('ALM02.1','O alarme '+ str(_alarmeTipo_id) + ' já está ativo')
                print('ALM02.1: O alarme '+ str(_codigoAlarme) + ' já está ativo')
                return True
            if(len(alm)>1):
                log('ALM02.2','Erro, existe mais de um alarme do tipo: '
                + str(_codigoAlarme) + ' ativo, inativando os mais velhos')
                for x in range(len(alm)-1):
                    alm[x].tempoInativacao=int(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                return True
        except Exception as e:
            log('ALM02.3',str(e))
            return False

        #Caso nenhum problema aconteceu, insere um novo alarme na tabela
        try:
            Alarme(codigoAlarme=_codigoAlarme,
                mensagemAlarme = _mensagemAlarme,
                prioridadeAlarme = _prioridadeAlarme,
                ativo=True, syncAtivacao=False,
                ambiente_id=_ambiente,
                tempoAtivacao=datetime.datetime.fromtimestamp(time.time())
            ).save()

            return True
        except Exception as e:
            log('ALM02.4',str(e))
            return False

    def off(_codigoAlarme):
        try:
            #verifica se o codigo do alarme está ativo
            alm = Alarme.objects.\
                filter(codigoAlarme = _codigoAlarme, ativo = True)\
                .order_by('id').all()
            #O alarme já está ativo, desativa
            try:
                if(len(alm)>1):
                    log('ALM03.0','Erro, existe mais de um alarme do tipo: '
                        + str(_codigoAlarme) + ' ativo, inativando todos')
                if(len(alm)==0):
                    # log('ALM03.1','Não existe alarme do tipo: '+ str(_alarmeTipo_id) + ' ativo!')
                    print('ALM03.1: Não existe alarme do tipo: '+ str(_codigoAlarme) + ' ativo!')
                    return False
                for x in range(len(alm)):
                    #Altera alarme na tabela
                    alm[x].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                return True
            except Exception as e:
                log('ALM03.2',str(e))
                return False
        except Exception as e:
            log('ALM03.3',str(e))
            return False