import _thread
import serial
from log import log

class PlacaBase():
	def receber(self,porta,taxa,callback):
		try:
			self.ptser = serial.Serial(porta, taxa)
			_thread.start_new_thread(self.recebeMensagens, (self.ptser, callback))
		except Exception as e:
			log("PLB01", str(e))

	class recebeMensagens():
		def __init__(self, ser, callback):
			while(True):
				try:
					callback(ser.readline())
				except Exception as e:
					log("PLB02",str(e))

	def enviar(self, mensagem):
		try:
			self.ptser.write(bytes(mensagem, 'UTF-8'))
		except Exception as e:
			log("PLB03",str(e))

