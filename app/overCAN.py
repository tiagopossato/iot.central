from placaIO import alteraEstadoEntrada

ovcComands = { \
	'ONLINE' : 1,\
	'SEND_DATA' : 2,\
	'IS_ONLINE' : 3,\

	'SEND_CONFIG' : 10,\
	'CHANGE_ID' : 11,\
	'CHANGE_READ_TIME' : 12,\
	'CHANGE_SEND_TIME' : 13,\

	'SEND_TIME' : 21,\

	'CHANGE_OUTPUT_STATE' : 50,\

	'OUTPUT_1_STATE' : 51,\

	'INPUT_1_STATE' : 61,\
}

def digest(mensagem):
	#print(mensagem)
	if(mensagem['codigo']==ovcComands['INPUT_1_STATE']):
		inputState(mensagem['id'], mensagem['msg'][0])

"""
Recebe uma mensagem com os estados das entradas digitais
"""
def inputState(_idRede, _estados):
	#converte o valor recebido em um array de bits
	_estados = list(bin(_estados).split('b')[1][::-1])
	while(len(_estados)<8):
		_estados.insert(0,0)
	for x in range(len(_estados)):
		alteraEstadoEntrada(_codigoPlacaExpansaoDigital=int(_idRede), _numero=int(x), _estado=int(_estados[x]))






