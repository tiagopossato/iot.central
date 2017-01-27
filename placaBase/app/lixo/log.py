import os
import sys
import django
import datetime
import time

sys.path.insert(0, os.path.abspath('../../interface'))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()

from central.views import Log

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
	arquivo = open("/opt/iot.central/banco/logs.csv","+a")
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
