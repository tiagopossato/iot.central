from time import sleep
import requests
import os
from log import log
from configuracao import config
from Banco import getSession, removeSession, AlarmeTipo, Alarme

def _selecionaAlarmes():
	session = getSession()
	if session == False: return False
	try:
		alarmes = session.query(Alarme).filter(Alarme.syncAtivacao == False).all()
		_sincronizaAlarmes(session, alarmes, True)

		"""Apaga os alarmes mais antigos"""
		alarmes = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == True).order_by(Alarme.id.asc()).all()
		#apaga a quantidade de registros com id mais antigo já sincronizados
		for x in range(len(alarmes)-config['maxAlarmes']):
			session.delete(alarmes[x])
			session.commit()

		alarmes = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == False).all()
		_sincronizaAlarmes(session, alarmes, False)

		"""Apaga os alarmes mais antigos"""
		alarmes = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == True).order_by(Alarme.id.asc()).all()
		#apaga a quantidade de registros com id mais antigo já sincronizados
		for x in range(len(alarmes)-config['maxAlarmes']):
			session.delete(alarmes[x])
			session.commit()

	except Exception as e:
		log('SCA01', str(e))
	finally:
		removeSession()


def _sincronizaAlarmes(session, alarmes, novo):
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
						session.commit()
					else:
						log('SCA01',str(r))
				except Exception as e:
					log('SCA02',str(e))
					session.rollback()
					if type(e).__name__ == "ConnectionError":
						return
			else:
				try:
					headers = {'uuid': config['uuid']}
					r = requests.put(config['enderecoServidor'] + '/api/alarme', dados, verify=False, headers=headers)
					if r.status_code == 201:
						alarmes[x].syncInativacao = True
						session.commit()
					else:
						log('SCA03',str(r))
				except Exception as e:
					log('SCA04',str(e))
					session.rollback()
					if type(e).__name__ == "ConnectionError":
						return

	except Exception as e:
		log('SCA05',str(e))
		session.rollback()
		removeSession()
		return False

if __name__ == "__main__":
	try:
		arquivo = open("/var/run/centralSinc.pid","w")
		pid = os.getpid()
		arquivo.write(str(pid))
		print(pid)
		arquivo.close()
	except PermissionError as e:
		print("Executar como root!")
		print(e)
		exit()

	try:
		while(True):
			_selecionaAlarmes()
			sleep(0.5)
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		print("Saindo...")
