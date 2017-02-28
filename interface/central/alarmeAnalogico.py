import datetime
import time
from central.log import log
from central.alarmeTrigger import alarmeTrigger
from central.models import AlarmeAnalogico, Leitura, Sensor

def newAlarmeAnalogico(_mensagemAlarme, _prioridadeAlarme,
                        _valorAlarmeOn, _valorAlarmeOff,
                        _ambiente_id, _grandeza_id):
    try:
        AlarmeAnalogico(mensagemAlarme = _mensagemAlarme, prioridadeAlarme = _prioridadeAlarme,
                            valorAlarmeOn = _valorAlarmeOn, valorAlarmeOff=_valorAlarmeOff,
                            ambiente_id = _ambiente_id, grandeza_id = _grandeza_id
                        ).save()
    except Exception as e:
        log('AAN01.0',str(e))

def updateAlarmeAnalogico(_codigoAlarme, _mensagemAlarme, _prioridadeAlarme,
                        _valorAlarmeOn, _valorAlarmeOff,
                        _ambiente_id, _grandeza_id):
    try:
        alm = EntradaDigital.objects.get(codigoAlarme = _codigoAlarme)

        alm.mensagemAlarme = _mensagemAlarme
        alm.prioridadeAlarme = _prioridadeAlarme
        alm.valorAlarmeOn = _valorAlarmeOn
        alm.valorAlarmeOff=_valorAlarmeOff
        alm.ambiente_id = _ambiente_id
        alm.grandeza_id = _grandeza_id
        alm.save()
    except Exception as e:
        log('AAN02.0',str(e))

def triggerAlarmeAnalogico(_grandeza, _ambiente):
    try:
        alarmes =  AlarmeAnalogico.objects.filter(grandeza= _grandeza, ambiente = _ambiente)
        if(len(alarmes)==0): return
    except Exception as e:
        log('AAN03.0',str(e))
    
    """
    Pega a última leitura de cada sensor dessa grandeza na última hora neste ambiente
    """
    try:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts-3600) #3600 segundos = 1 hora
        et = datetime.datetime.fromtimestamp(ts)
        # print(st.strftime('%Y-%m-%d %H:%M:%S') + ' - '+ et.strftime('%Y-%m-%d %H:%M:%S'))
        #seleciona os sensores que enviaram dados na ultima hora
        sensores = Leitura.objects.filter(
                                grandeza=_grandeza, ambiente=_ambiente, created_at__range=(st, et)
                                ).values_list('sensor', flat=True).distinct()
    except Exception as e:
        log('AAN03.1',str(e))
    
    try:
        listaMedia = []
        ts = time.time()
        et = datetime.datetime.fromtimestamp(ts)
        for sensor in sensores:
            sensor = Sensor.objects.get(idRede=sensor)      
            # A data inicial da consulta é o tempo atual menos o intervaloAtualizacao de atualização do sensor,
            # desta forma, se o sensor não está enviando dados atualizados, os seus valores não serão incluídos 
            # no cálculo da média
            st = datetime.datetime.fromtimestamp(ts-sensor.intervaloAtualizacao)
            leitura = Leitura.objects.filter(
                                grandeza=_grandeza, ambiente=_ambiente,
                                created_at__range=(st, et), sensor = sensor
                                ).last()
            if(leitura != None): listaMedia.append(leitura)
        
        soma = 0
        total = len(listaMedia)
        for x in range(total):
            soma = soma + listaMedia[x].valor
        
        valorMedio = soma / total
    except Exception as e:
        log('AAN03.2',str(e))
    
    try:
        print('Média: ' + str(valorMedio))
        alarmes = AlarmeAnalogico.objects.filter(ambiente=_ambiente)
        for alarme in alarmes:            
            # Para cada alarme neste ambiente, verifica se o valor para ligar o alarme é maior que o valor para desligar o alarme
            if(alarme.valorAlarmeOn > alarme.valorAlarmeOff):
                # Se sim, significa que o alarme vai disparar com valores acima do valor para ligar o alarme
                if(valorMedio > alarme.valorAlarmeOn):
                    # Se a média é maior que o valor para ligar o alarme, dispara o método para ligar o alarme
                    alarmeTrigger.on(_codigoAlarme=alarme.codigoAlarme,
                                        _mensagemAlarme=alarme.mensagemAlarme,
                                        _prioridadeAlarme=alarme.prioridadeAlarme,
                                        _ambiente=_ambiente.id)
                if(valorMedio < alarme.valorAlarmeOff):
                    # Se a média é menor que o valor para desligar o alarme, dispara o método para desligar o alarme
                    alarmeTrigger.off(_codigoAlarme=alarme.codigoAlarme)
            if(alarme.valorAlarmeOn < alarme.valorAlarmeOff):
                # Se não, significa que o alarme vai disparar com valores abaixo do valor para ligar o alarme
                if(valorMedio < alarme.valorAlarmeOn):
                    # Se a média é menor que o valor para ligar o alarme, dispara o método para ligar o alarme
                    alarmeTrigger.on(_codigoAlarme=alarme.codigoAlarme,
                                        _mensagemAlarme=alarme.mensagemAlarme,
                                        _prioridadeAlarme=alarme.prioridadeAlarme,
                                        _ambiente=_ambiente.id)
                if(valorMedio > alarme.valorAlarmeOn):
                    # Se a média é maior que o valor para desligar o alarme, dispara o método para desligar o alarme
                    alarmeTrigger.off(_codigoAlarme=alarme.codigoAlarme)
    except Exception as e:
        log('AAN03.3',str(e))
