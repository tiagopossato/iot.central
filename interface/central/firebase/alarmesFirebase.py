import pyrebase
import requests
import time
import datetime
from threading import Thread
from central.models import AlarmeTipo, Alarme
from central.log import log
from central.models import Configuracoes
from placaBase.configuracao import config

class SincronizaAlarmes(Thread):
    def __init__ (self): 
        self.conectaFirebase()
        Thread.__init__(self)

    def conectaFirebase(self):
        try:
            self.cfg = Configuracoes.objects.get()
            config = {
                "apiKey": self.cfg.apiKey,
                "authDomain": self.cfg.authDomain,
                "databaseURL": self.cfg.databaseURL,
                "storageBucket": self.cfg.storageBucket
            }
            self.firebase = pyrebase.initialize_app(config)
            # Get a reference to the auth service
            self.auth = self.firebase.auth()
            # Get a reference to the database service
            self.db = self.firebase.database()
        except Exception as e:
            print('conectaFirebase')
            print(e)
            return

        try:
            # Log the user in
            self.user = self.auth.sign_in_with_email_and_password(self.cfg.email, self.cfg.senha)
        except requests.exceptions.HTTPError as e:
            e = eval(e.strerror)
            log('AFB01.0',e['error']['message'])
        except Exception as e:            
            log('AFB01.1',str(e))
                                
    def run(self):
        try:
            self.user = self.auth.refresh(self.user['refreshToken'])            
        except Exception as e:
            log('AFB02.0',str(e))
            self.conectaFirebase()
       
        #pega os alarmes novos, que ainda não foram criados
        #no banco de dados do servidor
        try:
            #primeiro os ativos
            alarmes = Alarme.objects.filter(syncAtivacao = False, syncInativacao = False).order_by('-ativo')
            # print("Enviando novos alarmes ainda ativos")
            self._enviaAlarmes(alarmes)
        except Exception as e:
            log('AFB02.1',str(e))

        try:
            alarmes = Alarme.objects.filter(syncInativacao = False)
            # print("Enviando novos alarmes que já desativaram")
            self._enviaAlarmes(alarmes)
        except Exception as e:
            log('AFB02.2',str(e))

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

    def _enviaAlarmes(self, alarmes):
        try:
            #monta uma mensagem com cada alarme
            for x in range(len(alarmes)):
                #se o ambiente do alarme não possuir uid, não envia o alarme para o servidor
                if(alarmes[x].ambiente.uid==None or alarmes[x].ambiente.uid == ''): continue

                dados = {}

                dados['ativo'] = alarmes[x].ativo

                if alarmes[x].tempoInativacao:
                    dados['tempoInativacao'] = alarmes[x].tempoInativacao.strftime('%Y-%m-%d %H:%M:%S.%f')

                if alarmes[x].alarmeTipo.prioridade:
                    dados['prioridade'] = alarmes[x].alarmeTipo.prioridade
                else:
                    dados['prioridade'] = 0

                dados['mensagem'] = alarmes[x].alarmeTipo.mensagem

                dados['tempoAtivacao'] = alarmes[x].tempoAtivacao.strftime('%Y-%m-%d %H:%M:%S.%f')
               
                #verifica se o alarme já foi cadastrado no banco 
                if(alarmes[x].uid):
                    alm = self.db.child("alarmes").child(alarmes[x].uid).set(dados, self.user['idToken'])
                    alarmes[x].syncAtivacao = True
                    alarmes[x].syncInativacao = True
                    alarmes[x].save()
                else:
                    alm = self.db.child("alarmes").push(dados, self.user['idToken'])
                    self.db.child("ambientes").child(alarmes[x].ambiente.uid).child("alarmes").child(alm['name']).set(True, self.user['idToken'])
                    alarmes[x].uid = alm['name']
                    alarmes[x].syncAtivacao = True
                    alarmes[x].save()

        except Exception as e:
            log('AFB03.0',str(e))
            return False
