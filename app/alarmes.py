# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import time
import datetime
import requests
from log import log

session = None
Base = declarative_base()

url = 'http://localhost:8080/api/alarme'

class AlarmeTipo(Base):
	__tablename__ = 'alarmeTipos'
	# Here we define columns for the table
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	codigo = Column(Integer, nullable=False, unique=True)
	mensagem = Column(String(255), nullable=False, unique=True)
	prioridade = Column(Integer, nullable=False)

class Alarme(Base):
	__tablename__ = 'alarmes'
	# Here we define columns for the table
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	ativo = Column(Boolean, nullable=False)
	tempoAtivacao = Column(DateTime, nullable=False)
	syncAtivacao = Column(Boolean, nullable=False, default=False)
	tempoInativacao = Column(DateTime)
	syncInativacao = Column(Boolean, nullable=False, default=False)

	codigoAlarme = Column(Integer, ForeignKey('alarmeTipos.codigo'))
	alarmeTipo = relationship(AlarmeTipo)

#Funcao para ativar chaves estrangeiras no banco
def _fk_pragma_on_connect(dbapi_con, con_record):
	dbapi_con.execute('pragma foreign_keys=ON')

def inicializa():
	global session
	if session: return True
	try:
		# Cria ou abre o banco
		engine = create_engine('sqlite:////opt/iot.central/Banco/alarmes.sqlite')
		event.listen(engine, 'connect', _fk_pragma_on_connect)

		# Create all tables in the engine. This is equivalent to "Create Table"
		# statements in raw SQL.
		Base.metadata.create_all(engine)

		# Bind the engine to the metadata of the Base class so that the
		# declaratives can be accessed through a DBSession instance
		Base.metadata.bind = engine

		DBSession = sessionmaker(bind=engine)
		#Uma instância DBSession () estabelece todas as conversas com o banco de dados
		#e representa uma "zona de teste" para todos os objetos carregados no objeto 
		#de sessão do banco de dados. 
		#Qualquer alteração feita nos objetos na sessão não será persistente no
		#banco de dados até que seja chamado session.commit().
		#Se você não está feliz com as alterações, você pode reverter todas 
		#elas de volta para o último commit chamando session.rollback()
		session = DBSession()
		return True
	except Exception as e:
		log('ALM01',str(e))
		return False

class newAlarmType():
	def __init__(self, _codigo, _mensagem, _prioridade):
		global session
		if inicializa() == False: return None
		try:
			at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
			session.add(at)
			session.commit()
		except Exception as e:
			log('ALM02',str(e))
			#desfaz as alterações na sessão
			session.rollback()			
			session = None

class alarmTrigger():
	def on(codigo):
		global session
		if inicializa() == False: return None
		try:
			#verifica se o codigo do alarme já está ativo
			at = session.query(Alarme).filter(Alarme.codigoAlarme == codigo).filter(Alarme.ativo == True).all()
			if len(at) == 1:
				#O alarme já está ativo
				log('ALM03','O alarme já está ativo')
				return True
		except Exception as e:
			log('ALM04',str(e))
			session.rollback()
			return False

		try:
			#Insere um novo alarme na tabela
			a = Alarme(codigoAlarme=codigo, ativo=True, tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
			session.add(a)
			session.commit()
			sincronizaAlarmes()
			return True
		except Exception as e:
			session.rollback()
			log('ALM05',str(e))
			return False

	def off(codigo):
		if inicializa() == False: return False
		try:
			#verifica se o codigo do alarme já está ativo
			alm = session.query(Alarme).filter(Alarme.codigoAlarme == codigo).filter(Alarme.ativo == True).all()
			if len(alm) == 1:
				#O alarme já está ativo, desativa
				try:
					#Altera alarme na tabela
					alm[0].tempoInativacao=datetime.datetime.fromtimestamp(time.time())
					alm[0].ativo = False
					alm[0].syncInativacao = False
					session.commit()
					sincronizaAlarmes(False)
					return True
				except Exception as e:
					session.rollback()
					log('ALM06',str(e))
					return False
			else:
				#O alarme não está ativo
				return False
		except Exception as e:
			log('ALM07',str(e))
			session.rollback()
			return False

def sincronizaAlarmes(_completo=True):
	if inicializa() == False: return False
	try:

		if _completo:
			alm = session.query(Alarme).filter(Alarme.syncAtivacao == False).all()
		else:
			alm = session.query(Alarme).filter(Alarme.syncAtivacao == True).filter(Alarme.syncInativacao == False).all()

		for x in range(len(alm)):
			dados = {}
			
			dados['id'] = alm[x].id
			dados['ativo'] = alm[x].ativo
			if alm[x].tempoInativacao: 
				dados['tempoInativacao'] = alm[x].tempoInativacao.strftime('%Y-%m-%d %H:%M:%S.%f')

			if _completo:
				if alm[x].alarmeTipo.prioridade:
					dados['prioridade'] = alm[x].alarmeTipo.prioridade

				if alm[x].alarmeTipo.mensagem:
					dados['mensagem'] = alm[x].alarmeTipo.mensagem
			

				if alm[x].tempoAtivacao: 
					dados['tempoAtivacao'] = alm[x].tempoAtivacao.strftime('%Y-%m-%d %H:%M:%S.%f')
			
				#print(dados)
				try:
					r = requests.post(url, dados)
					if r.status_code == 201:
						alm[x].syncAtivacao = True
						alm[x].syncInativacao = True
						session.commit()
					else:
						log('ALM08',str(r))
				except Exception as e:
					log('ALM09',str(e))
					session.rollback()
			else:
				print(dados)
				try:
					r = requests.put(url, dados)
					if r.status_code == 201:
						alm[x].syncInativacao = True
						session.commit()
					else:
						log('ALM10',str(r))
				except Exception as e:
					log('ALM11',str(e))
					session.rollback()
	except Exception as e:
		log('ALM12',str(e))
		session.rollback()
		return False

	if _completo == False:
		sincronizaAlarmes(True)
