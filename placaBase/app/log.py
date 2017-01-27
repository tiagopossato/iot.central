# -*- coding: utf-8 -*-
import sqlite3
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import time
import datetime
import os

Session = None

Base = declarative_base()

class Log(Base):
	__tablename__ = 'log'
	# Here we define columns for the table
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	tipo = Column(String(6))
	mensagem = Column(String(255), nullable=False)
	sync = Column(Boolean, nullable=False, default=False)
	tempo = Column(DateTime, nullable=False)

def _init():
	global Session
	if Session != None: return
	try:
		# Cria ou abre o banco
		engine = create_engine('sqlite:////opt/iot.central/Banco/logs.sqlite')

		# Create all tables in the engine. This is equivalent to "Create Table"
		# statements in raw SQL.
		Base.metadata.create_all(engine)

		# Bind the engine to the metadata of the Base class so that the
		# declaratives can be accessed through a DBSession instance
		Base.metadata.bind = engine

		session_factory = sessionmaker(bind=engine)
		#Uma instância DBSession () estabelece todas as conversas com o banco de dados
		#e representa uma "zona de teste" para todos os objetos carregados no objeto 
		#de sessão do banco de dados. 
		#Qualquer alteração feita nos objetos na sessão não será persistente no
		#banco de dados até que seja chamado session.commit().
		#Se você não está feliz com as alterações, você pode reverter todas 
		#elas de volta para o último commit chamando session.rollback()
		Session = scoped_session(session_factory)
	except Exception as e:
		salvaArquivo('LOG01', str(e))
		return False

def removeSession():
	global Session
	_init()
	Session.remove()

def getSession():
	global Session
	_init()
	s = Session()
	return s

class log():
	def __init__(self,_tipo, _mensagem):
		session = getSession()
		if session == False: return False
		try:
			lg = Log(mensagem=_mensagem, tipo = _tipo, tempo = datetime.datetime.fromtimestamp(time.time()))
			session.add(lg)
			session.commit()
			print('['+ datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')\
			+ '] [' + _tipo + '] [' + _mensagem + ']')
		except Exception as e:
			salvaArquivo(_tipo, _mensagem)
			salvaArquivo('LOG02', str(e))
			#desfaz as alterações na sessão
			session.rollback()
		finally:
			removeSession()

def salvaArquivo(_tipo, _mensagem):
	arquivo = open("/opt/iot.central/Banco/logs.csv","+a")
	arquivo.write('[')
	arquivo.write(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
	arquivo.write('] [')
	arquivo.write(_tipo)
	arquivo.write('] [')
	arquivo.write(_mensagem)
	arquivo.write(']\n')
	arquivo.close()
	print('['+ datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')\
	+ '] [' + _tipo + '] [' + _mensagem + ']')






