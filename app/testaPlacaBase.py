#!/usr/bin/python3
from placaBase import PlacaBase
import serial
from time import sleep
from random import randint

pb = PlacaBase()
pb.iniciar('/dev/ttyACM0', 115200, lambda msg: print(msg))
tempo = 1

def pbTeste():
	pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))

while(True):
	try:
		entrada = input()

		if(entrada == '1'):
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,1))
		if(entrada == '2'):
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,0))
		if(entrada == '3'):
			pb.enviaComando('3', 'CHANGE_SEND_TIME', "1")
			pb.enviaComando('2', 'CHANGE_SEND_TIME', "1")
		if(entrada == '4'):
			pb.enviaComando('3', 'CHANGE_SEND_TIME', "255")
			pb.enviaComando('2', 'CHANGE_SEND_TIME', "255")
		if(entrada == '5'):
			pb.enviaComando('0', 'IS_ONLINE')
		if(entrada == '-'):
			pb.resetPlacaBase()

	except (KeyboardInterrupt):
		for x in range(8):
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
		print("saindo, aguarde!")
		sleep(1)
		pb.fechar()
		exit()

while(True):
	for x in range(8):
		try:
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (randint(0,8),randint(0,1)))
		except KeyboardInterrupt:
			for x in range(8):
				pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
			pb.join()
			exit()
	#sleep(tempo)

def pbOff():
	for x in range(8):
		pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
		#sleep(0.01)

c = 5
while(c>0):
	try:
		pbTeste()
		c = c - 1
		#sleep(0.25)
	except KeyboardInterrupt:
		pbOff()
		exit()

pbOff()

