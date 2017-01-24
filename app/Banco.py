# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import time
import datetime
from log import log

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
	id = Column(Integer, primary_key=True)
	ativo = Column(Boolean, nullable=False)
	tempoAtivacao = Column(DateTime, nullable=False)
	syncAtivacao = Column(Boolean, nullable=False, default=False)
	tempoInativacao = Column(DateTime)
	syncInativacao = Column(Boolean, nullable=False, default=False)

	codigoAlarme = Column(Integer, ForeignKey('alarmeTipos.codigo'))
	alarmeTipo = relationship(AlarmeTipo)

class PlacaExpansaoDigital(Base):
	__tablename__ = 'placaExpansaoDigitais'
	id = Column(Integer, primary_key=True)
	idRede = Column(Integer, nullable=False, unique=True)
	updated_at = Column(DateTime, default=datetime.datetime.fromtimestamp(time.time()))

class EntradaDigital(Base):
	__tablename__ = 'entradasDigitais'
	id = Column(Integer, primary_key=True)
	numero = Column(Integer, nullable=False)
	nome = Column(String(255), nullable=False)
	estado = Column(Boolean, nullable=False, default=False)
	updated_at = Column(DateTime, default= datetime.datetime.fromtimestamp(time.time()))
	sync = Column(Boolean, nullable=False, default=False)

	codigoPlacaExpansaoDigital = Column(Integer, ForeignKey('placaExpansaoDigitais.idRede'))
	placaExpansaoDigital = relationship(PlacaExpansaoDigital)

	codigoAlarme = Column(Integer, ForeignKey('alarmeTipos.codigo'), nullable=True, default=None)
	#alarmeTipo = relationship(AlarmeTipo)

#Funcao para ativar chaves estrangeiras no banco
def _fk_pragma_on_connect(dbapi_con, con_record):
	dbapi_con.execute('pragma foreign_keys=ON')

def getSession():
	try:
		# Cria ou abre o banco
		engine = create_engine('sqlite:////opt/iot.central/Banco/central.sqlite')
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
		return session
	except Exception as e:
		log('PLI01',str(e))
		return False
