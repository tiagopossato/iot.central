import datetime
import time
from django.utils import timezone
from central.settings import TIME_ZONE


def triggerAlarmeAnalogico(_grandeza, _ambiente):
    """
    Gatilho dos alarmes analógicos
    """
    from aplicacao.log import log
    from aplicacao.models import AlarmeAnalogico, Leitura, Sensor

    timezone.activate(TIME_ZONE)

    try:
        alarmes = AlarmeAnalogico.objects.filter(
            grandeza=_grandeza, ambiente=_ambiente)
        if(len(alarmes) == 0):
            return
        # print(alarmes)
    except Exception as e:
        log('ALMAN', str(e))
        return

    # Pega a última leitura de cada sensor dessa grandeza na última hora neste ambiente
    try:
        endTime = timezone.localtime()
        startTime = endTime - datetime.timedelta(hours=1)
        # print(st.strftime('%Y-%m-%d %H:%M:%S') + ' - '+ et.strftime('%Y-%m-%d %H:%M:%S'))
        # seleciona os sensores que enviaram dados na ultima hora
        sensores = Leitura.objects.filter(
            grandeza=_grandeza, ambiente=_ambiente, createdAt__range=(
                startTime, endTime)
        ).values_list('sensor', flat=True).distinct()
    except Exception as e:
        log('AAN03.1', str(e))
        return
    try:
        listaMedia = []
        # ts = time.time()
        # et = datetime.datetime.fromtimestamp(ts)
        endTime = timezone.localtime()
        for sensor in sensores:
            sensor = Sensor.objects.get(uid=str(sensor))
            # A data inicial da consulta é o tempo atual menos duas vezes o intervaloAtualizacao de atualização do sensor,
            # desta forma, se o sensor não está enviando dados atualizados, os seus valores não serão incluídos
            # no cálculo da média
            # st = datetime.datetime.fromtimestamp(ts-sensor.intervaloAtualizacao)
            startTime = endTime - \
                datetime.timedelta(seconds=(sensor.intervaloLeitura * 2))
            leitura = Leitura.objects.filter(
                grandeza=_grandeza, ambiente=_ambiente,
                createdAt__range=(startTime, endTime), sensor=sensor
            ).last()
            if(leitura != None):
                listaMedia.append(leitura)

        soma = 0
        total = len(listaMedia)
        for x in range(total):
            soma = soma + listaMedia[x].valor

        valorMedio = soma / total
    except Exception as e:
        log('AAN03.2', str(e))
        return

    try:
        # print('Media: ' + str(valorMedio))
        # alarmes = AlarmeAnalogico.objects.filter(ambiente=_ambiente)
        for alarme in alarmes:
            # Para cada alarme neste ambiente, verifica se o valor para ligar o alarme é maior que o valor para desligar o alarme
            if(alarme.valorAlarmeOn > alarme.valorAlarmeOff):
                # Se sim, significa que o alarme vai disparar com valores acima do valor para ligar o alarme
                if(valorMedio > alarme.valorAlarmeOn):
                    # Se a média é maior que o valor para ligar o alarme, dispara o método para ligar o alarme
                    alarmeTrigger.on(_codigoAlarme=alarme.codigoAlarme,
                                     _mensagemAlarme=alarme.mensagemAlarme,
                                     _prioridadeAlarme=alarme.prioridadeAlarme,
                                     _ambiente=_ambiente.uid,
                                     _grandeza=_grandeza)
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
                                     _ambiente=_ambiente.uid,
                                     _grandeza=_grandeza)
                if(valorMedio > alarme.valorAlarmeOn):
                    # Se a média é maior que o valor para desligar o alarme, dispara o método para desligar o alarme
                    alarmeTrigger.off(_codigoAlarme=alarme.codigoAlarme)
    except Exception as e:
        log('AAN03.3', str(e))


class alarmeTrigger():
    def on(_codigoAlarme, _mensagemAlarme, _prioridadeAlarme, _ambiente, _grandeza):
        from aplicacao.log import log
        from aplicacao.models import Alarme

        try:
            # verifica se o codigo do alarme já está ativo
            alm = Alarme.objects.\
                filter(codigoAlarme=_codigoAlarme, ativo=True)\
                .order_by('uid').all()
        except Exception as e:
            log('ALT01.0', str(e))
            return False
        try:
            if(len(alm) == 1):
                # O alarme já está ativo
                # log('ALT01.1','O alarme '+ str(_alarmeTipo_id) + ' já está ativo')
                # print('ALT01.1: O alarme '+ str(_codigoAlarme) + ' ja esta ativo')
                return True
            if(len(alm) > 1):
                log('ALT01.2', 'Erro, existe mais de um alarme do tipo: '
                    + str(_codigoAlarme) + ' ativo, inativando os mais velhos')
                for x in range(len(alm) - 1):
                    alm[x].tempoInativacao = timezone.localtime()
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()
                return True
        except Exception as e:
            log('ALT01.3', str(e))
            return False

        # Caso nenhum problema aconteceu, insere um novo alarme na tabela
        try:
            alm = Alarme(codigoAlarme=_codigoAlarme,
                         mensagemAlarme=_mensagemAlarme,
                         prioridadeAlarme=_prioridadeAlarme,
                         ativo=True,
                         syncAtivacao=False,
                         ambiente_id=_ambiente,
                         grandeza=_grandeza,
                         tempoAtivacao=timezone.localtime()
                         )
            alm.save()
            print('ON: ' + str(alm))

            return True
        except Exception as e:
            log('ALT01.4', str(e))
            return False

    def off(_codigoAlarme):
        from aplicacao.log import log
        from aplicacao.models import Alarme

        try:
            # verifica se o codigo do alarme está ativo
            alm = Alarme.objects.\
                filter(codigoAlarme=_codigoAlarme, ativo=True)\
                .order_by('uid').all()
            # O alarme já está ativo, desativa
            try:
                if(len(alm) > 1):
                    log('AT02.0', 'Erro, existe mais de um alarme do tipo: '
                        + str(_codigoAlarme) + ' ativo, inativando todos')
                if(len(alm) == 0):
                    # log('ALT02.1','Não existe alarme do tipo: '+ str(_alarmeTipo_id) + ' ativo!')
                    # print('ALT02.1: Nao existe alarme do tipo: '+ str(_codigoAlarme) + ' ativo!')
                    return False
                for x in range(len(alm)):
                    # Altera alarme na tabela
                    alm[x].tempoInativacao = timezone.localtime()
                    alm[x].ativo = False
                    alm[x].syncInativacao = False
                    alm[x].save()

                    print('OFF: ' + str(alm[x]))
                return True
            except Exception as e:
                log('ALT02.2', str(e))
                return False
        except Exception as e:
            log('ALT02.3', str(e))
            return False
