import time
import datetime
import requests
from log import log
from configuracao import config
from Banco import getSession, PlacaExpansaoDigital, EntradaDigital, AlarmeTipo
from alarmes import alarmTrigger

def newPlacaExpansaoDigital(_idRede):
	session = getSession()
	if session == False: return False
	try:
		pli = PlacaExpansaoDigital(idRede=_idRede)
		session.add(pli)
		session.commit()
	except Exception as e:
		log('PLI02',str(e))
		#desfaz as alterações na sessão
		session.rollback()
		session = None

def newEntradaDigital(_codigoPlacaExpansaoDigital, _numero, _codigoAlarme, _nome = ""):
	session = getSession()
	if session == False: return False
	try:
		entrada = session.query(EntradaDigital)\
			.filter(EntradaDigital.numero == _numero)\
			.filter(EntradaDigital.codigoPlacaExpansaoDigital ==_codigoPlacaExpansaoDigital)\
			.all()
		if(len(entrada)>0):
			log('PLI03.0', "Entrada já cadastrada!")
			return False
	
		entrada = EntradaDigital(numero=_numero, codigoPlacaExpansaoDigital=_codigoPlacaExpansaoDigital, nome=_nome, codigoAlarme = _codigoAlarme)
		session.add(entrada)
		session.commit()
	except Exception as e:
		log('PLI03',str(e))
		#desfaz as alterações na sessão
		session.rollback()
		session = None

def updateEntradaDigital(_id, _codigoPlacaExpansaoDigital=None, _numero=None, _codigoAlarme=-1, _nome=None):
	session = getSession()
	if session == False: return False
	try:
		entrada = session.query(EntradaDigital).filter(EntradaDigital.id == _id).one()
		try:
			if(_codigoPlacaExpansaoDigital != None): entrada.codigoPlacaExpansaoDigital = _codigoPlacaExpansaoDigital
			if(_numero != None): entrada.numero = _numero
			if(_codigoAlarme != -1): entrada.codigoAlarme = _codigoAlarme
			if(_codigoAlarme == -1): entrada.codigoAlarme = None
			if(_nome != None): entrada.nome = _nome

			entrada.updated_at = datetime.datetime.fromtimestamp(time.time())
			session.commit()
			return True
		except Exception as e:
			session.rollback()
			log('PLI04.0',str(e))
			return False
	except Exception as e:
		log('PLI04.1',str(e))
		session.rollback()
	return False

def alteraEstadoEntrada(_codigoPlacaExpansaoDigital, _numero, _estado):
	session = getSession()
	if session == False: return False
	try:
		entrada = session.query(EntradaDigital)\
			.filter(EntradaDigital.codigoPlacaExpansaoDigital == _codigoPlacaExpansaoDigital)\
			.filter(EntradaDigital.numero == _numero)\
			.one()
		if(int(entrada.estado) != int(_estado)):
			print("Update no "+entrada.nome+" -> "+str(_estado))
			print()
			if(int(_estado)==1):
				entrada.estado = True
			else:
				entrada.estado = False
			entrada.sync = False
			entrada.updated_at = datetime.datetime.fromtimestamp(time.time())
			session.commit()
			if(entrada.codigoAlarme != None and entrada.codigoAlarme != ''):
				if(_estado == True): alarmTrigger.on(entrada.codigoAlarme)
				if(_estado == False): alarmTrigger.off(entrada.codigoAlarme)
		return True
	except Exception as e:
		log('PLI05.0',str(e))
		session.rollback()
	return False

