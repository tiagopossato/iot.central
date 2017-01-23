import _thread
import serial
import simplejson
from log import log
from overCAN import ovcComands

class PlacaBase():
	def receber(self,porta,taxa,callback):
		try:
			self.ptser = serial.Serial()
			self.ptser.port = porta
			self.ptser.baudrate = taxa
			self.ptser.parity=serial.PARITY_NONE
			self.ptser.stopbits=serial.STOPBITS_ONE
			self.ptser.bytesize=serial.EIGHTBITS
			self.ptser.timeout=1
			self.ptser.open()

			_thread.start_new_thread(self.recebeMensagens, (self.ptser, callback))
		except Exception as e:
			log("PLB01", str(e))

	class recebeMensagens():
		def __init__(self, ser, callback):
			while(True):
				try:
					inMsg = ser.readline().decode("UTF-8")
					if(len(inMsg) == 0 ):
						continue
					try:
						j = simplejson.loads(inMsg)
						callback(j)
					except simplejson.scanner.JSONDecodeError as e:
						#retira a ultima virgula da string
						#inMsg = inMsg[:len(inMsg) - inMsg[::-1].find(',')-1] + inMsg[len(inMsg) - inMsg[::-1].find(','):]
						log("PLB02.1",str(e) + "["+inMsg+"]")
				except Exception as e:
					log("PLB02.2",str(e))

	def __enviar__(self, mensagem):
		mensagem += '\n'
		print(mensagem)
		try:
			while(self.ptser.isOpen() == False): pass
			self.ptser.write(bytes(mensagem, 'UTF-8'))
		except Exception as e:
			log("PLB03",str(e))

	def enviaComando(self, id, comando, msg = ''):
		try:
			strComando = str(int(id))
			strComando += ':'
			strComando += str(ovcComands[comando])
			strComando += ':'
			if(isinstance(msg, str)):
				strComando += str(msg)
			elif(isinstance(msg, tuple)):
					for x in range(len(msg)):
						strComando += str(msg[x]) + ":"
			else:
				log("PLB04.1","O parâmetro msg deve ser uma única string ou uma tupla de strings")
				return False
			self.__enviar__(strComando)
		except ValueError as e:
			log("PLB04.2",str(e))
		#except KeyError as e:
		#	log("PLB05",str(e))










