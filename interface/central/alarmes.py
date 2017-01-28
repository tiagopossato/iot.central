import datetime
import time
import requests
from threading import Thread

from configuracao import config
from central.models import AlarmeTipo, Alarme
from central.log import log

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
        self.sincronizador = _SincronizaAlarmes()
        self.sincronizador.start()

    def on(self, _alarmeTipo_id):
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
                    alm[x].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                    if(self.sincronizador.isAlive() == False):
                        self.sincronizador.run()
        except Exception as e:
            print(e)
            log('ALM03',str(e))
            return False
        #Insere um novo alarme na tabela
        try:
            a = Alarme(alarmeTipo_id=_alarmeTipo_id, ativo=True, syncAtivacao=False, tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
            a.save()
            if(self.sincronizador.isAlive() == False):
                self.sincronizador.run()
            return True
        except Exception as e:
            log('ALM04',str(e))
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
                    log('ALM05.0','Erro, existe mais de um alarme do tipo: '\
                    + str(_alarmeTipo_id) + ' ativo, inativando todos')
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
                log('ALM05.2',str(e))
                return False
        except Alarme.DoesNotExist:
            #O alarme não está ativo
            return False
        except Exception as e:
            log('ALM06',str(e))
            return False

class _SincronizaAlarmes(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        # def sincronizaAlarmes():
        #pega os alarmes novos, que ainda não foram criados
        #no banco de dados do servidor
        try:
            #primeiro os ativos
            alarmes = Alarme.objects.filter(syncAtivacao = False, ativo = True)
            # print("Enviando novos alarmes ainda ativos")
            self._enviaAlarmes(alarmes, True)

            alarmes = Alarme.objects.filter(syncAtivacao = False)
            # print("Enviando novos alarmes que já desativaram")
            self._enviaAlarmes(alarmes, True)
        except Alarme.DoesNotExist:
            pass
        except Exception as e:
            log('ALM07',str(e))

        try:
            #Apaga os alarmes mais antigos
            #a ordenação dos resultados de forma ascentende já é implícita
            #https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao = True).order_by('id')
            # print("Enviando alarmes desativados")
            #apaga a quantidade de registros com id mais antigo já sincronizados
            for x in range(len(alarmes)-config['maxAlarmes']):
                alarmes[x].delete()
        except Alarme.DoesNotExist:
            pass
        except Exception as e:
            log('ALM08',str(e))

        #pega os alarmes que já foram criados, mas existem alterações para
        #serem feitas
        try:
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao= False)
            self._enviaAlarmes(alarmes, False)
        except Alarme.DoesNotExist:
            pass
        except Exception as e:
            log('ALM09',str(e))

        try:
            #Apaga os alarmes mais antigos
            #a ordenação dos resultados de forma ascentende já é implícita
            #https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao = True).order_by('id')
            #apaga a quantidade de registros com id mais antigo já sincronizados
            for x in range(len(alarmes)-config['maxAlarmes']):
                alarmes[x].delete()
        except Alarme.DoesNotExist:
            pass
        except Exception as e:
            log('ALM08',str(e))


    def _enviaAlarmes(self, alarmes, novo):
        try:
            for x in range(len(alarmes)):
                dados = {}

                dados['id'] = alarmes[x].id
                dados['ativo'] = alarmes[x].ativo

                if alarmes[x].tempoInativacao:
                    dados['tempoInativacao'] = alarmes[x].tempoInativacao.strftime('%Y-%m-%d %H:%M:%S.%f')

                if novo:
                    if alarmes[x].alarmeTipo.prioridade:
                        dados['prioridade'] = alarmes[x].alarmeTipo.prioridade

                    if alarmes[x].alarmeTipo.mensagem:
                        dados['mensagem'] = alarmes[x].alarmeTipo.mensagem

                    if alarmes[x].tempoAtivacao:
                        dados['tempoAtivacao'] = alarmes[x].tempoAtivacao.strftime('%Y-%m-%d %H:%M:%S.%f')

                    try:
                        headers = {'uuid': config['uuid']}
                        r = requests.post(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
                        if r.status_code == 201:
                            alarmes[x].syncAtivacao = True
                            alarmes[x].syncInativacao = True
                            alarmes[x].save()
                        else:
                            log('ALM10',str(r))
                    except Exception as e:
                        log('ALM11',str(e))
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
                            log('ALM12',str(r))
                    except Exception as e:
                        log('ALM12',str(e))
                        if type(e).__name__ == "ConnectionError":
                            return

        except Exception as e:
            log('ALM13',str(e))
            return False
