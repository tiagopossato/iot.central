import os
import sys
import django
from random import randint
from time import time, sleep
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(__file__ ,"../../..")))
os.environ["DJANGO_SETTINGS_MODULE"] = "interface.settings"
django.setup()
#importacoes depois do setup do django
from central.log import log
from central.models import SaidaDigital
from central.models import Configuracoes
from central.placaBase.overCAN import processaMensagem
from central.placaBase.placaBase import PlacaBase

try:
    cfg = Configuracoes.objects.get()
    PlacaBase.iniciar(cfg.portaSerial, cfg.taxa, processaMensagem)
except Exception as e:
    log('CEN01.0', str(e))

log('START', 'Serviço da central iniciado')

def triggerSaidasDigitais():
    #Consultar banco de dados (django.db)

    #Chamar funcao de acionamento (temporizacao como parametro)

    while (True):

        tsd = SaidaDigital.objects.filter(ativa=True).all()

        registros = len(tsd)
        #Nao sei a funcao time() retorna o timestamp ja corrigido em -10800 (3 Horas) devido ao fuso horario
        horaAtual = datetime.fromtimestamp(time())
        #print(horaAtual)

        try:

            if (registros == 0):
                sleep(1)
                continue

            for x in range(registros):

                #Verifica o estado (se estiver ligado ou desligado)
                #SE nao houver ultimo acionamento definido OU
                #A diferenca (delta) entre a hora atual e o ultimo acionamento for menor ou igual ao tempo desligado


                if (not tsd[x].estado):

                    if (tsd[x].tempoLigado == 0):
                        continue

                    delta = (horaAtual - tsd[x].ultimoAcionamento).total_seconds()

                    if ((tsd[x].ultimoAcionamento == datetime.fromtimestamp(0)) or
                                (delta >= (tsd[x].tempoDesligado + tsd[x].tempoLigado))):

                        tsd[x].ultimoAcionamento = horaAtual
                        tsd[x].estado = True
                        tsd[x].save()
                        tsd[x].ligar()
                else:

                    if (tsd[x].tempoDesligado == 0):
                        continue

                    delta = (horaAtual - tsd[x].updatedAt).total_seconds()

                    if (delta >= tsd[x].tempoLigado):
                        tsd[x].estado = False
                        tsd[x].save()
                        tsd[x].desligar()

            #Espera por 0.25 segundos
            sleep(0.25)

        except Exception as e:
            log('CEN02.0', str(e))
            continue

triggerSaidasDigitais()
