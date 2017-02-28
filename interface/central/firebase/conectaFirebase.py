import pyrebase
import requests
import os
from central.log import log
from central.models import Configuracoes
from central.util import check_host

class ConectaFirebase:
    auth = None
    db = None
    _user = None
    _token = None

    def __init__(self):
        try:
            if(check_host()==False):
                log('CFB01.0',"Sem conexão")
                return None
            cfg = Configuracoes.objects.get()            
            config = {
                "apiKey": cfg.apiKey,
                "authDomain": cfg.authDomain,
                "databaseURL": cfg.databaseURL,
                "storageBucket": cfg.storageBucket,
                "serviceAccount": os.path.dirname(os.path.abspath(__file__)) + '/testes-apiSensores-cba45d38c53e.json'
            }   
            firebase = pyrebase.initialize_app(config)
            # Get a reference to the auth service
            ConectaFirebase.auth = firebase.auth()
            # Get a reference to the database service
            ConectaFirebase.db = firebase.database()
        except Exception as e:
            log('CFB01.1',str(e))
            return None
    
    def getUser():
        try:
            cfg = Configuracoes.objects.get()
            if(ConectaFirebase._token==None): 
                ConectaFirebase._token= ConectaFirebase.auth.create_custom_token(cfg.uidCentral)
            ConectaFirebase._user = ConectaFirebase.auth.sign_in_with_custom_token(ConectaFirebase._token)
            return ConectaFirebase._user
        except requests.exceptions.HTTPError as e:
            e = eval(e.strerror)
            log('CFB01.2',e['error']['message'])
            return False
        except Exception as e:
            log('CFB01.3',str(e))
            return False