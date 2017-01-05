import requests
import time
import datetime

url = 'http://localhost:8080/api/alarme'

class Alarme():
	id = None
	mensagem = None
	prioridade = 0
	ativo = True
	tempoAtivacao = None
	tempoInativacao = None
	reconhecido = False
	tempoReconhecido = None
	mensagemReconhecido = None

	def postAlarme(self):
		r = requests.post(url, self.__dict__)
		print(r.status_code)
		print(r.content)
	pass


def getAlarmes():
	r = requests.get(url)
	print(r.content)
pass


al = Alarme()
al.id = 2
al.prioridade = 3
al.tempoAtivacao = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
al.mensagem = 'Temperatura da câmara fria 2 acima do estabelecido'

#postAlarme(al)

#getAlarmes()


