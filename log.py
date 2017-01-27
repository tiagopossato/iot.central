import os
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.interface.settings"
import django
django.setup()
from interface.logs.models import Log
import datetime
import time
import os
class log():
	def __init__(self,_tipo, _mensagem):
		try:
			lg = Log(mensagem=_mensagem, tipo = _tipo)
			lg.save()
			print(Log.objects.all())
			print('['+ datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')\
			+ '] [' + _tipo + '] [' + _mensagem + ']')
		except Exception as e:
			salvaArquivo(_tipo, _mensagem)
			salvaArquivo('LOG02', str(e))

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






