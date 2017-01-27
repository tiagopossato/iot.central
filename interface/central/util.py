import os
import datetime
import time

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
