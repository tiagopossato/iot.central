# -*- coding: utf-8 -*-
import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import time
import datetime

session = None

Base = declarative_base()

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
	sync = Column(Boolean, nullable=False, default=False)
	tempoAtivacao = Column(DateTime, nullable=False)
	tempoInativacao = Column(DateTime)

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
		engine = create_engine('sqlite:///Banco/alarmes.sqlite')
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
		print('Erro alm01')
		print(e)
		return False

class newAlarmType():
	def __init__(self, _codigo, _mensagem, _prioridade):
		global session
		if inicializa() == False: return False
		try:
			at = AlarmeTipo(codigo=_codigo, mensagem=_mensagem, prioridade=_prioridade)
			session.add(at)
			session.commit()
		except Exception as e:
			print('Erro alm02')
			print(e)
			#desfaz as alterações na sessão
			session.rollback()			
			session = None

class alarmTrigger():
	def on(codigo):
		global session
		if inicializa() == False: return False
		try:
			#verifica se o codigo do alarme já está ativo
			at = session.query(Alarme).filter(Alarme.codigoAlarme == codigo).filter(Alarme.ativo == True).all()
			if len(at) == 1:
				#O alarme já está ativo
				print('O alarme já está ativo')
				return True
		except Exception as e:
			print('Erro alm03')
			print(e)
			session.rollback()
			return False

		try:
			#Insere um novo alarme na tabela
			a = Alarme(codigoAlarme=codigo, ativo=True, tempoAtivacao=datetime.datetime.fromtimestamp(time.time()))
			session.add(a)
			session.commit()
			print('Novo alarme inserido!')
			return True
		except Exception as e:
			session.rollback()
			print('Erro alm04')
			print(e)
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
					session.commit()
					print('Alarme desativado!')
					return True
				except Exception as e:
					session.rollback()
					print('Erro alm05')
					print(e)
					return False
			else:
				#O alarme não está ativo
				print('O alarme não está ativo')
				return False
		except Exception as e:
			print('Erro alm06')
			print(e)
			session.rollback()
			return False
