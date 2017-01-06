import time

from alarmes import alarmTrigger
from log import log

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
exit()

