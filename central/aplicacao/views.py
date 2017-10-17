from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
from central.settings import TIME_ZONE
from interface.decorators import ajax_login_required
from datetime import datetime, timedelta, time
from aplicacao.models import Ambiente, Sensor, Grandeza, SensorGrandeza, Leitura
import json
from django.utils.dateformat import format

@login_required(login_url='/login')
def grafico(request):
    return render(request, 'aplicacao/leituras.html')

@login_required(login_url='/login')
def leituras(request):
    end_date = timezone.now()
    start_date = end_date - timedelta(hours=12)

    # leituras = Leitura.objects.filter(createdAt__range=(start_date, end_date), sensor_id='7e0f933d-75a9-42f3-bb98-207a2ad4d13a')
    # leituras = Leitura.objects.filter(createdAt__range=(start_date, end_date), sensor_id='8c5710ab-36b3-4f20-a9fc-798229983c80')
    leituras = Leitura.objects.filter(createdAt__range=(start_date, end_date), sensor__active=True)
  


    # ambientes = leituras.values('ambiente').distinct()
    # grandezas = leituras.values('grandeza').distinct()
    sensores = leituras.values('sensor').distinct()

    saida = []
    # for s in sensores:
    #     ss = {}        
    #     sen = Sensor.objects.get(uid=s['sensor'])
    #     ss['descricao'] = sen.descricao
    #     ss['ambiente'] = sen.ambiente.nome
    #     ss['grandezas'] = []        
    #     sgs = SensorGrandeza.objects.filter(sensor=sen)
    #     for g in sgs:
    #         gg = {}
    #         gg['nome'] = g.grandeza.nome
    #         gg['unidade'] = g.grandeza.unidade
    #         gg['leituras'] = []
    #         try:
    #             for l in leituras.filter(ambiente=sen.ambiente, sensor=sen, grandeza=g.grandeza):
    #                 k = {}
    #                 k['valor'] = l.valor
    #                 k['createdAt'] = str(l.createdAt)
    #                 gg['leituras'].append(k)
    #         except Exception as e:
    #             print(e)
    #         ss['grandezas'].append(gg)        
    #     saida.append(ss)

    for s in sensores:
        ss = {}        
        sen = Sensor.objects.get(uid=s['sensor'])
        ss['d'] = sen.descricao
        ss['a'] = sen.ambiente.nome
        ss['g'] = []        
        sgs = SensorGrandeza.objects.filter(sensor=sen)
        for g in sgs:
            gg = {}
            gg['n'] = g.grandeza.nome
            gg['u'] = g.grandeza.unidade
            gg['l'] = []
            try:
                for l in leituras.filter(ambiente=sen.ambiente, sensor=sen, grandeza=g.grandeza):
                    k = {}
                    k['v'] = l.valor
                    k['c'] = int(format(l.createdAt, 'U'))
                    # k['c'] = str(l.createdAt)
                    gg['l'].append(k)
            except Exception as e:
                print(e)
            ss['g'].append(gg)
        saida.append(ss)

    return HttpResponse(
                json.dumps(saida),
                content_type='application/json; charset=utf8'
                )
