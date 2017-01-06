# -*- coding: utf-8 -*-
import sqlite3
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
import datetime

session = None

Base = declarative_base()

class Log(Base):
	__tablename__ = 'log'
	# Here we define columns for the table
	# Notice that each column is also a normal Python instance attribute.
	id = Column(Integer, primary_key=True)
	mensagem = Column(String(255), nullable=False)
	sync = Column(Boolean, nullable=False, default=False)
	tempo = Column(DateTime, nullable=False)

def inicializa():
	global session
	if session: return True
	try:
		# Cria ou abre o banco
		engine = create_engine('sqlite:///Banco/logs.sqlite')

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
		print(e)
		return False

class log():
	def __init__(self,_mensagem):
		global session
		if inicializa() == False: return False
		try:
			lg = Log(mensagem=_mensagem, tempo = datetime.datetime.fromtimestamp(time.time()))
			session.add(lg)
			session.commit()
		except Exception as e:
			print('Erro log01')
			print(e)
			#desfaz as alterações na sessão
			session.rollback()
			session = None
