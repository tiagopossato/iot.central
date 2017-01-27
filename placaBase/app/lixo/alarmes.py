from threading import Thread
import time
import datetime
import requests
from log import log
from configuracao import config
from Banco import getSession, removeSession, AlarmeTipo, Alarme

def newAlarmeTipo(_codigo, _mensagem, _prioridade):
    session = getSession()
    if session == False: return False
    try:
        at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
        session.add(at)
        session.commit()
    except Exception as e:
        log('ALM02',str(e))
        #desfaz as alterações na sessão
        session.rollback()
        session = None
    finally:
        removeSession()

class alarmTrigger():
    def on(codigo):
        session = getSession()
        if session == False: return False
        try:
            #verifica se o codigo do alarme já está ativo
            at = session.query(Alarme).filter(Alarme.codigoAlarme == codigo).filter(Alarme.ativo == True).all()
            if len(at) == 1:
                #O alarme já está ativo
                log('ALM03','O alarme já está ativo')
                return True
        except Exception as e:
            log('ALM04',str(e))
            session.rollback()
            removeSession()
            return False

        try:
            #Insere um novo alarme na tabela
            a = Alarme(codigoAlarme=codigo, ativo=True, syncAtivacao=False, tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
            session.add(a)
            session.commit()
            #_SincronizaAlarmes(_completo=True).start()
            return True
        except Exception as e:
            session.rollback()
            log('ALM05',str(e))
            return False
        finally:
            removeSession()

    def off(codigo):
        session = getSession()
        if session == False: return False
        try:
            #verifica se o codigo do alarme já está ativo
            alm = session.query(Alarme).filter(Alarme.codigoAlarme == codigo).filter(Alarme.ativo == True).all()
            if len(alm) == 1:
                #O alarme já está ativo, desativa
                try:
                    #Altera alarme na tabela
                    alm[0].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                    alm[0].ativo = False
                    alm[0].syncInativacao = False
                    session.commit()
                    #_SincronizaAlarmes(_completo=False).start()
                    return True
                except Exception as e:
                    session.rollback()
                    removeSession()
                    log('ALM06',str(e))
                    return False
            else:
                #O alarme não está ativo
                return False
        except Exception as e:
            log('ALM07',str(e))
            session.rollback()
            return False
        finally:
            removeSession()
"""
class _SincronizaAlarmes(Thread):

    def __init__ (self, _completo=True):
        self.completo=_completo
        Thread.__init__(self)

    def run(self):
        session = getSession()
        if session == False: return False
        try:

            if self.completo:
                alm = session.query(Alarme).filter(Alarme.syncAtivacao == False).all()
            else:
                alm = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == False).all()

            for x in range(len(alm)):
                dados = {}

                dados['id'] = alm[x].id
                dados['ativo'] = alm[x].ativo
                if alm[x].tempoInativacao:
                    dados['tempoInativacao'] = alm[x].tempoInativacao.strftime('%Y-%m-%d %H:%M:%S.%f')

                if self.completo:
                    if alm[x].alarmeTipo.prioridade:
                        dados['prioridade'] = alm[x].alarmeTipo.prioridade

                    if alm[x].alarmeTipo.mensagem:
                        dados['mensagem'] = alm[x].alarmeTipo.mensagem


                    if alm[x].tempoAtivacao:
                        dados['tempoAtivacao'] = alm[x].tempoAtivacao.strftime('%Y-%m-%d %H:%M:%S.%f')

                    #print(dados)
                    try:
                        headers = {'uuid': config['uuid']}
                        r = requests.post(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
                        if r.status_code == 201:
                            alm[x].syncAtivacao = True
                            alm[x].syncInativacao = True
                            session.commit()
                        else:
                            log('ALM08',str(r))
                    except Exception as e:
                        log('ALM09',str(e))
                        session.rollback()
                        if type(e).__name__ == "ConnectionError":
                            return
                else:
                    print(dados)
                    try:
                        headers = {'uuid': config['uuid']}
                        r = requests.put(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
                        if r.status_code == 201:
                            alm[x].syncInativacao = True
                            session.commit()
                        else:
                            log('ALM10',str(r))
                    except Exception as e:
                        log('ALM11',str(e))
                        session.rollback()
                        if type(e).__name__ == "ConnectionError":
                            return
        except Exception as e:
            log('ALM12',str(e))
            session.rollback()
            removeSession()
            return False

        if self.completo == False:
            self.completo = True
            self.run()

        #Apaga os alarmes mais antidos
        alms = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == True).order_by(Alarme.id.asc()).all()
        #apaga a quantidade de registros com id mais antigo já sincronizados
        for x in range(len(alms)-config['maxAlarmes']):
            session.delete(alms[x])
        session.commit()
        removeSession()
"""
