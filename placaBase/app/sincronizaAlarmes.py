import os
import sys
import django
sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from time import sleep
from central.log import log
from configuracao import config
from central.alarmes import sincronizaAlarmes

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
		while(True):
			sincronizaAlarmes()
			sleep(2)
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		print("Saindo...")
