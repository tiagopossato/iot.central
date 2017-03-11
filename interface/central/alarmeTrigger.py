import datetime
import time
from central.models import Alarme, Ambiente
from central.log import log

class alarmeTrigger():

    def on(_codigoAlarme, _mensagemAlarme, _prioridadeAlarme, _ambiente):
        try:
            #verifica se o codigo do alarme já está ativo
            alm = Alarme.objects.\
                filter(codigoAlarme = _codigoAlarme, ativo = True)\
                .order_by('id').all()
        except Exception as e:
            log('ALT01.0',str(e))
            return False
        print(alm)
        try:
            if(len(alm)==1):
                #O alarme já está ativo
                # log('ALT01.1','O alarme '+ str(_alarmeTipo_id) + ' já está ativo')
                #print('ALT01.1: O alarme '+ str(_codigoAlarme) + ' já está ativo')
                return True
            if(len(alm)>1):
                log('ALT01.2','Erro, existe mais de um alarme do tipo: '
                + str(_codigoAlarme) + ' ativo, inativando os mais velhos')
                for x in range(len(alm)-1):
                    alm[x].tempoInativacao=int(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                return True
        except Exception as e:
            log('ALT01.3',str(e))
            return False

        #Caso nenhum problema aconteceu, insere um novo alarme na tabela
        try:
            alm = Alarme(codigoAlarme=_codigoAlarme,
                mensagemAlarme = _mensagemAlarme,
                prioridadeAlarme = _prioridadeAlarme,
                ativo=True, syncAtivacao=False,
                ambiente_id=_ambiente,
                tempoAtivacao=datetime.datetime.fromtimestamp(time.time())
            )
            alm.save()
            print(alm)

            return True
        except Exception as e:
            log('ALT01.4',str(e))
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
                    log('AT02.0','Erro, existe mais de um alarme do tipo: '
                        + str(_codigoAlarme) + ' ativo, inativando todos')
                if(len(alm)==0):
                    # log('ALT02.1','Não existe alarme do tipo: '+ str(_alarmeTipo_id) + ' ativo!')
                    #print('ALT02.1: Não existe alarme do tipo: '+ str(_codigoAlarme) + ' ativo!')
                    return False
                for x in range(len(alm)):
                    #Altera alarme na tabela
                    alm[x].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                return True
            except Exception as e:
                log('ALT02.2',str(e))
                return False
        except Exception as e:
            log('ALT02.3',str(e))
            return False
