from placaBase import PlacaBase

pb = PlacaBase()
pb.receber('/dev/ttyACM0', 115200, lambda msg: print(msg))

while(True):
	try:
		entrada = str(input('Comando: '))
		pb.enviar(entrada+'\n')
	except (KeyboardInterrupt):
		print("saindo..")
		exit()
