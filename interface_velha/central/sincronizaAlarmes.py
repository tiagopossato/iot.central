import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.join(__file__ ,"../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from time import sleep
from central.log import log
from central.firebase.alarmesFirebase import SincronizaAlarmes


if __name__ == "__main__":
	# try:
	# 	arquivo = open("/var/run/centralSinc.pid","w")
	# 	pid = os.getpid()
	# 	arquivo.write(str(pid))
	# 	print(pid)
	# 	arquivo.close()
	# except PermissionError as e:
	# 	print("Executar como root!")
	# 	print(e)
	# 	exit()

	try:
		sincronizador = SincronizaAlarmes()
		sincronizador.start()
		while(True):
			if(sincronizador.isAlive() == False):
				sincronizador.run()
			sleep(0.1)
	except Exception as e:
		print("Sincronizador...")
		print(e)
	except KeyboardInterrupt:
		print("Saindo...")