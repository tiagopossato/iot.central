import pyrebase
import requests
from central.log import log
from central.models import Configuracoes
from central.util import check_host

class ConectaFirebase:
    auth = None
    db = None

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
                "serviceAccount": "../testes-apiSensores-cba45d38c53e.json"
            }
            firebase = pyrebase.initialize_app(config)
            # Get a reference to the auth service
            ConectaFirebase.auth = firebase.auth()
            # Get a reference to the database service
            ConectaFirebase.db = firebase.database()
        except Exception as e:
            log('CFB01.1',str(e))
            return None
    
    def user():
        try:
            cfg = Configuracoes.objects.get()
            token = ConectaFirebase.auth.create_custom_token(cfg.uidCentral)
            ConectaFirebase.user = ConectaFirebase.auth.sign_in_with_custom_token(token)
            return ConectaFirebase.user
        except requests.exceptions.HTTPError as e:
            e = eval(e.strerror)
            log('CFB01.2',e['error']['message'])
            return False
        except Exception as e:
            log('CFB01.3',str(e))
            return False