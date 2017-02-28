from central.firebase.conectaFirebase import ConectaFirebase

def salvaFirebase(ambiente):
    try:
        print('Nome: ' + ambiente.nome)
        ConectaFirebase()
        user = ConectaFirebase.user()
        db = ConectaFirebase.db
        amb = db.child("ambientes").push({'nome':ambiente.nome}, user['idToken'])
        ambiente.uid = amb['name']
        return ambiente
    except Exception as e:
        print('salvaFirebase: ' + str(e))
        # raise e