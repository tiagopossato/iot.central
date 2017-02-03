import datetime
import time
import requests
from threading import Thread

from configuracao import config
from central.models import AlarmeTipo, Alarme, Ambiente
from central.log import log

from central.firebase.alarmesFirebase import SincronizaAlarmes

"""
Cria um novo tipo de alarme
"""
def newAlarmeTipo(_codigo, _mensagem, _prioridade):
    try:
        at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
        at.save()
    except Exception as e:
        log('ALM01',str(e))

class AlarmTrigger():
    def __init__(self):
        self.sincronizador = SincronizaAlarmes()
        self.sincronizador.start()

    def on(self, _alarmeTipo_id, _ambiente):
        try:
            #verifica se o codigo do alarme já está ativo
            alm = Alarme.objects.\
                filter(alarmeTipo_id = _alarmeTipo_id, ativo = True)\
                .order_by('id').all()

            if(len(alm)==1):
                #O alarme já está ativo
                log('ALM02.0','O alarme já está ativo')
                return True
            if(len(alm)>1):
                log('ALM02.1','Erro, existe mais de um alarme do tipo: '\
                + str(_alarmeTipo_id) + ' ativo, inativando os mais velhos')
                for x in range(len(alm)-1):
                    alm[x].tempoInativacao=int(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                    if(self.sincronizador.isAlive() == False):
                        self.sincronizador.run()
                return True
        except Exception as e:
            print(e)
            log('ALM02.2',str(e))
            return False

        #Caso nenhum problema aconteceu, insere um novo alarme na tabela
        try:
            ambiente = Ambiente.objects.only('id').get(id=_ambiente)
            a = Alarme(alarmeTipo_id=_alarmeTipo_id, \
                ativo=True, syncAtivacao=False, \
                ambiente=ambiente,\
                tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
            a.save()

            if(self.sincronizador.isAlive() == False):
                self.sincronizador.run()
            return True
        except Exception as e:
            log('ALM02.3',str(e))
            return False

    def off(self, _alarmeTipo_id):
        try:
            #verifica se o codigo do alarme está ativo
            alm = Alarme.objects.\
                filter(alarmeTipo_id = _alarmeTipo_id, ativo = True)\
                .order_by('id').all()
            #O alarme já está ativo, desativa
            try:
                if(len(alm)>1):
                    log('ALM03.0','Erro, existe mais de um alarme do tipo: '\
                    + str(_alarmeTipo_id) + ' ativo, inativando todos')
                if(len(alm)==0):
                    log('ALM03.1','Não existe alarme do tipo: '\
                    + str(_alarmeTipo_id) + ' ativo!')
                    return False
                for x in range(len(alm)):
                    #Altera alarme na tabela
                    alm[x].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                    if(self.sincronizador.isAlive() == False):
                        self.sincronizador.run()
                return True
            except Exception as e:
                log('ALM03.2',str(e))
                return False
        except Exception as e:
            log('ALM03.3',str(e))
            return False

class _SincronizaAlarmes(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        #pega os alarmes novos, que ainda não foram criados
        #no banco de dados do servidor
        try:
            #primeiro os ativos
            alarmes = Alarme.objects.filter(syncAtivacao = False, ativo = True)
            # print("Enviando novos alarmes ainda ativos")
            self._enviaAlarmes(alarmes, True)
        except Exception as e:
            log('ALM04.0',str(e))

        try:
            alarmes = Alarme.objects.filter(syncAtivacao = False)
            # print("Enviando novos alarmes que já desativaram")
            self._enviaAlarmes(alarmes, True)
        except Exception as e:
            log('ALM04.1',str(e))

        try:
            #Apaga os alarmes mais antigos
            #a ordenação dos resultados de forma ascentende já é implícita
            #https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao = True).order_by('id')
            #apaga a quantidade de registros com id mais antigo já sincronizados
            for x in range(len(alarmes)-config['maxAlarmes']):
                alarmes[x].delete()
        except Exception as e:
            log('ALM04.2',str(e))

        #pega os alarmes que já foram criados, mas existem alterações para
        #serem feitas
        try:
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao= False)
            self._enviaAlarmes(alarmes, False)
        except Exception as e:
            log('ALM04.3',str(e))

        try:
            #Apaga os alarmes mais antigos
            #a ordenação dos resultados de forma ascentende já é implícita
            #https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao = True).order_by('id')
            #apaga a quantidade de registros com id mais antigo já sincronizados
            for x in range(len(alarmes)-config['maxAlarmes']):
                alarmes[x].delete()
        except Exception as e:
            log('ALM05.3',str(e))

    def _enviaAlarmes(self, alarmes, novo):
        try:
            #monta uma mensagem com cada alarme
            for x in range(len(alarmes)):
                dados = {}

                dados['id'] = alarmes[x].id
                dados['ativo'] = alarmes[x].ativo

                if alarmes[x].tempoInativacao:
                    dados['tempoInativacao'] = alarmes[x].tempoInativacao

                if novo:
                    if alarmes[x].alarmeTipo.prioridade:
                        dados['prioridade'] = alarmes[x].alarmeTipo.prioridade

                    if alarmes[x].alarmeTipo.mensagem:
                        dados['mensagem'] = alarmes[x].alarmeTipo.mensagem

                    if alarmes[x].tempoAtivacao:
                        dados['tempoAtivacao'] = alarmes[x].tempoAtivacao

                    try:
                        headers = {'uuid': config['uuid']}
                        r = requests.post(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
                        if r.status_code == 201:
                            alarmes[x].syncAtivacao = True
                            alarmes[x].syncInativacao = True
                            alarmes[x].save()
                        else:
                            log('ALM6.0',str(r))
                    except Exception as e:
                        log('ALM6.1',str(e))
                        if type(e).__name__ == "ConnectionError":
                            return
                else:
                    try:
                        headers = {'uuid': config['uuid']}
                        r = requests.put(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
                        if r.status_code == 201:
                            alarmes[x].syncInativacao = True
                            alarmes[x].save()
                        else:
                            log('ALM6.2',str(r))
                    except Exception as e:
                        log('ALM6.3',str(e))
                        if type(e).__name__ == "ConnectionError":
                            return

        except Exception as e:
            log('ALM6.4',str(e))
            return False
