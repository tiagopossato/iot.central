from central.firebase.conectaFirebase import ConectaFirebase
from central.models import Configuracoes

def novoAmbienteFirebase(ambiente):
    try:
        ConectaFirebase()
        user = ConectaFirebase.getUser()
        db = ConectaFirebase.db
        dados = {}
        dados['nome'] = ambiente.nome
        dados['ativo'] = ambiente.ativo
        dados['createdAt'] = ambiente.createdAt.timestamp()
        dados['central'] = Configuracoes.objects.get().uidCentral
        print(dados)
        amb = db.child("ambientes").push(dados, user['idToken'])
        db.child("centrais").child(dados['central']).child('ambientes').child(amb['name']).set(True, user['idToken'])
        db.child("empresas").child(dados['central']).child('ambientes').child(amb['name']).set(True, user['idToken'])
        ambiente.uid = amb['name']
        return ambiente
    except Exception as e:   
        print(e.strerror)
        return False

def alteraAmbienteFirebase(ambiente):
    try:
        dados = {}
        dados['nome'] = ambiente.nome
        dados['ativo'] = ambiente.ativo
        dados['createdAt'] = ambiente.createdAt.timestamp()
        dados['updatedAt'] = ambiente.updatedAt.timestamp()
        dados['central'] = Configuracoes.objects.get().uidCentral
        print(dados)
        ConectaFirebase()
        user = ConectaFirebase.getUser()
        db = ConectaFirebase.db
        amb = db.child("ambientes").child(ambiente.uid).set(dados, user['idToken'])
        return ambiente      
    except Exception as e:
        print('alteraAmbienteFirebase: ' + str(e))
        return False
