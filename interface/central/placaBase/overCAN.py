from central.placaIO import alteraEstadoEntrada
from central.sensor import newLeitura
from central.log import log

ovcComands = {
    'ONLINE' : 1,
    'SEND_DATA' : 2,
    'IS_ONLINE' : 3,

    'SEND_CONFIG' : 10,
    'CHANGE_ID' : 11,
    'CHANGE_READ_TIME' : 12,
    'CHANGE_SEND_TIME' : 13,

    'SEND_TIME' : 21,

    'CHANGE_OUTPUT_STATE' : 50,

    'OUTPUT_1_STATE' : 51,

    'INPUT_1_STATE' : 61,

    'ANALOG_VALUE' : 70,
}

tipoGrandeza = {
    'entradaDigital' : 3200,
    'saidaDigital' : 3201,
    'entradaAnalogica' : 3202,
    'especial' : 9999,
}

grandeza = {
    'online' : 1,
    'temperatura' : 3303,
    'umidadeAr' : 3304,
    'umidadeSolo' : 3320,
}

def processaMensagem(mensagem):
    # print(mensagem)
    if(mensagem['tipoGrandeza'] == tipoGrandeza['entradaDigital']):
        alteraEstadoEntrada(_codigoPlacaExpansaoDigital=int(mensagem['id']),
                            _numero=mensagem['grandeza',
                            _estado=int(mensagem['valor']))
        return True

    if(mensagem['tipoGrandeza'] == tipoGrandeza['entradaAnalogica']):
         newLeitura(_idRedeSensor=int(mensagem['id']),
                    _grandeza=mensagem['grandeza'],
                    _valor=mensagem['valor'])
        return True

    if(mensagem['tipoGrandeza'] == tipoGrandeza['especial'] and mensagem['grandeza'] == grandeza['online']):
        log('ONLINE','Dispositivo ' + str(mensagem['id']) + ' esta online')

"""
Recebe uma mensagem com os estados das entradas digitais
"""
def inputState(_idRede, _estados):
    #print(_estados)
    #converte o valor recebido em um array de bits
    _estados = list(bin(_estados).split('b')[1])
    #print(_estados)
    #Caso o valor seja menor que 128
    #completa o array com os 8 bits
    while(len(_estados)<8):
        _estados.insert(0,0)
    _estados.reverse()
    print(_estados)
    for x in range(len(_estados)):
        #print("["+str(x) + "] : " + str(_estados[x]))
        alteraEstadoEntrada(_codigoPlacaExpansaoDigital=int(_idRede), _numero=int(x), _estado=int(_estados[x]))

"""
Recebe uma mensagem com um valor analógico
"""
def analogValue(_idRede, _mensagem):
    try:
        # print(_mensagem)
        valor = float(str(_mensagem[1])+'.'+ str(_mensagem[2]))
    except Exception as e:
        print(e)
        return False
    newLeitura(_idRedeSensor=_idRede,_grandeza=_mensagem[0], _valor=valor)
