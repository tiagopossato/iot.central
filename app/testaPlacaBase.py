from placaBase import PlacaBase
import serial
from time import sleep

pb = PlacaBase()
pb.receber('/dev/ttyACM0', 115200, lambda msg: print(msg))

while(True):
	try:
		entrada = input()
		if(entrada == '1'):
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,1))
		if(entrada == '2'):
			pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (0,0))
		if(entrada == '3'):
			pb.enviaComando('3', 'CHANGE_SEND_TIME', "1")
		if(entrada == '4'):
			pb.enviaComando('3', 'CHANGE_SEND_TIME', "255")

	except (KeyboardInterrupt):
		print("saindo..")
		exit()

while(True):
	for x in range(8):
		pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,1))
		sleep(0.1)
	for x in range(8):
		pb.enviaComando('3', 'CHANGE_OUTPUT_STATE', (x,0))
		sleep(0.1)
