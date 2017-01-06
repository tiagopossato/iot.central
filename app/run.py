import time
import sys
import os

from alarmes import alarmTrigger
from log import log

if __name__ == "__main__":
	try:
		arquivo = open("/var/run/central.pid","w")
		pid = os.getpid()
		arquivo.write(str(pid))
		print(pid)
		arquivo.close()
	except PermissionError as e:
		print("Executar como root!")
		print(e)
		exit()

	log("Iniciando aplicacao")
	while(True):
		try:	
			alarmTrigger.on(1)
			alarmTrigger.off(2)
			time.sleep(60)
			alarmTrigger.on(2)
			alarmTrigger.off(1)
			time.sleep(60)
		except (KeyboardInterrupt):
			print("saindo..")
			log("Encerrando aplicacao")
			exit()

