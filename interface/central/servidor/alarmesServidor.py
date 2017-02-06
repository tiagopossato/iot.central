import datetime
import time
import requests
from threading import Thread

from central.placaBase.configuracao import config
from central.models import AlarmeTipo, Alarme, Ambiente
from central.log import log

class SincronizaAlarmes(Thread):
    def __init__ (self):
        Thread.__init__(self)

    def run(self):
        #pega os alarmes novos, que ainda não foram criados
        #no banco de dados do servidor
        try:
            #primeiro os ativos
            alarmes = Alarme.objects.filter(syncAtivacao = False, syncInativacao = False).order_by('-ativo')
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
                            print(r.text)
                            log('ALM6.0',+','+r.text)
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
                            log('ALM6.2',str(r)+','+r.text)
                    except Exception as e:
                        log('ALM6.3',str(e))
                        if type(e).__name__ == "ConnectionError":
                            return

        except Exception as e:
            log('ALM6.4',str(e))
            return False
