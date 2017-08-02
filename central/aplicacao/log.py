import datetime
import time
from aplicacao.models import Log
from aplicacao.util import salvaArquivo

"""
Salva um log na tabela de logs
"""
def log(_tipo, _mensagem):
    try:
        lg = Log(mensagem=_mensagem, tipo = _tipo)
        lg.save()
        print('['+ datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')\
    + '] [' + _tipo + '] [' + _mensagem + ']')
    except Exception as e:
        salvaArquivo('LOG01', str(e))
        salvaArquivo(_tipo, _mensagem)
