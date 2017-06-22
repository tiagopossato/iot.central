import os
import sys
import django
from random import randint
from time import time, sleep
from datetime import datetime, time as dtTime

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()
# importacoes depois do setup do django
from central.log import log
from central.models import SaidaDigital
from central.models import Temporizador
from central.models import Configuracoes
from central.placaBase.overCAN import processaMensagem
from central.placaBase.placaBase import PlacaBase

try:
    cfg = Configuracoes.objects.get()
    PlacaBase.iniciar(cfg.portaSerial, cfg.taxa, processaMensagem)
except Exception as e:
    log('CEN01.0', str(e))

log('START', 'Servico da central iniciado')


def triggerSaidasDigitais():
    # Consultar banco de dados (django.db)

    # Chamar funcao de acionamento (temporizacao como parametro)

    while (True):

        saidas = SaidaDigital.objects.filter(ativa=True).all()

        registros = len(saidas)
        # Nao sei a funcao time() retorna o timestamp ja corrigido em -10800 (3 Horas) devido ao fuso horario
        horaAtual = datetime.time(datetime.fromtimestamp(time()))

        try:
            if (registros < 1):
                sleep(1)
                continue
            for x in range(registros):
                temporizador = Temporizador.objects.filter(saidaDigital_id=saidas[x].id, horaLigar__range=(
                    dtTime(00, 00, 0, 0), horaAtual), horaDesligar__range=(horaAtual, dtTime(23, 59, 59, 999999))).all()
                # print(str(temporizador.horaLigar))
                if(len(temporizador) > 0):
                    saidas[x].ligar()
                if(len(temporizador) <= 0):
                    saidas[x].desligar()
            # Espera por 1 segundos
            sleep(1)

        except Exception as e:
            log('CEN02.0', str(e))
            continue


triggerSaidasDigitais()
