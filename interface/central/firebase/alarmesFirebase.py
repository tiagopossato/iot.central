import pyrebase
import time
import datetime
import asyncio
from threading import Thread
from central.models import Alarme
from central.log import log
from central.models import Configuracoes
from central.firebase.conectaFirebase import ConectaFirebase
from central.util import check_host

class SincronizaAlarmes(Thread):
    def __init__ (self):        
        self.cfg = Configuracoes.objects.get()    
        ConectaFirebase()
        self.user = ConectaFirebase.user()
        self.db = ConectaFirebase.db
        Thread.__init__(self, name="SincronizaAlarmes")

    def run(self):
        print(Thread.getName(self))
        try:
            if(check_host()==False):
                print("Sem conexão")
                return
            self.user = ConectaFirebase.auth.refresh(self.user['refreshToken'])
        except Exception as e:
            log('AFB02.0',str(e))
            ConectaFirebase()
            self.user = ConectaFirebase.user()
            self.db = ConectaFirebase.db
            return
       
        try:        
            loop = asyncio.get_event_loop()
        except Exception as e:
            print("get_event_loop: " + str(e))
            return

        #pega os alarmes novos, que ainda não foram criados
        #no banco de dados do servidor            
        try:
            #primeiro os ativos
            alarmes = Alarme.objects.filter(syncAtivacao = False, syncInativacao = False).exclude(ambiente__uid = '').order_by('-ativo')
            #print("Enviando novos alarmes ainda ativos")
            for x in range(len(alarmes)):
                loop.call_soon(self._enviaAlarmes, loop, alarmes[x])
                loop.run_forever()
        except AssertionError as e:
            print(e)
        except Exception as e:
            log('AFB02.1',str(e))

        
        try:
            alarmes = Alarme.objects.filter(syncInativacao = False).exclude(ambiente__uid = '')
            # print("Enviando novos alarmes que já desativaram")
            for x in range(len(alarmes)):
                loop.call_soon(self._enviaAlarmes, loop, alarmes[x])
                loop.run_forever()
        except AssertionError as e:
            print(e)
        except Exception as e:
            log('AFB02.2',str(e))
        
        # try:        
        #     #loop.close()
        # except Exception as e:
        #     print("loop.close:" + str(e))
       

        try:
            #Apaga os alarmes mais antigos
            #a ordenação dos resultados de forma ascentende já é implícita
            #https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            alarmes = Alarme.objects.filter(syncAtivacao = True, syncInativacao = True).order_by('id')
            #apaga a quantidade de registros com id mais antigo já sincronizados
            for x in range(len(alarmes)-self.cfg.maxAlarmes):
                alarmes[x].delete()
        except Exception as e:
            log('AFB02.3',str(e))

    def _enviaAlarmes(self, loop, alarme):
        try:
            dados = {}

            dados['ativo'] = alarme.ativo

            if alarme.tempoInativacao:
                dados['tempoInativacao'] = alarme.tempoInativacao.strftime('%Y-%m-%d %H:%M:%S.%f')

            if alarme.prioridadeAlarme:
                dados['prioridade'] = alarme.prioridadeAlarme
            else:
                dados['prioridade'] = 0

            dados['mensagem'] = alarme.mensagemAlarme

            dados['tempoAtivacao'] = alarme.tempoAtivacao.strftime('%Y-%m-%d %H:%M:%S.%f')
            
            #verifica se o alarme já foi cadastrado no banco 
            if(alarme.uid):
                alm = self.db.child("alarmes").child(alarme.uid).set(dados, self.user['idToken'])
                alarme.syncAtivacao = True
                alarme.syncInativacao = True
                alarme.save()
            else:
                alm = self.db.child("alarmes").push(dados, self.user['idToken'])
                self.db.child("ambientes").child(alarme.ambiente.uid).child("alarmes").child(alm['name']).set(True, self.user['idToken'])
                alarme.uid = alm['name']
                alarme.syncAtivacao = True
                alarme.save()
            
            #encerra este loop
            loop.stop()
        except Exception as e:
            log('AFB03.0',str(e))
            loop.stop()            
