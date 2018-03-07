# -*- coding: utf 8 -*-

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
from django.db.models import Avg, Max, Min, Sum
from interface.decorators import ajax_login_required



@login_required(login_url='/login')
def leituras(request):
    ambientes = Ambiente.objects.all()
    return render(request, 'aplicacao/leituras.html', {'ambientes':ambientes})


@ajax_login_required
def metadados(request):
    if(request.method != 'GET'):
        return HttpResponseNotAllowed(['GET'])
    if(request.is_ajax() == False):
        return JsonResponse(status=400, data={'erro': "Somente requisicoes AJAX!"})
    try:
        id = request.GET.get('id')
        if(id == None):
            raise KeyError('id')
    except KeyError as e:
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})
    try:

        leituras = Leitura.objects.filter(ambiente_id=id)
        grandezasLidas = leituras.values('grandeza').distinct()
        
        grandezas = []
        for g in grandezasLidas:
            grandeza = Grandeza.objects.get(codigo=g['grandeza'])
            grandezaLeituras = leituras.filter(grandeza_id=grandeza.codigo)
            sensoresLidos = grandezaLeituras.values('sensor').distinct()
            sensores = []
            for s in sensoresLidos:
                sensor = Sensor.objects.get(uid=s['sensor'])
                sensorLeituras = grandezaLeituras.filter(sensor=sensor)
                maxDate = sensorLeituras.aggregate(Max('createdAt'))
                minDate = sensorLeituras.aggregate(Min('createdAt'))
                sensores.append({'uid':sensor.uid,
                                'descricao':sensor.descricao, 
                                'maxDate':maxDate['createdAt__max'],
                                'minDate':minDate['createdAt__min']
                                })
            grandezas.append({'codigo':grandeza.codigo, 'nome':grandeza.nome, 'sensores':sensores})

    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})
    
    try:
        return JsonResponse(status=200, data=grandezas, safe=False)
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})

@login_required(login_url='/login')
def grafico(request):
    if(request.method != 'GET'):
        return HttpResponseNotAllowed(['GET'])
    if(request.is_ajax() == False):
        return JsonResponse(status=400, data={'erro': "Somente requisicoes AJAX!"})
    try:
        ambiente_id = request.GET.get('ambiente')
        if(ambiente_id == None):
            raise KeyError('ambiente_id')
        grandeza_id = request.GET.get('grandeza')
        if(grandeza_id == None):
            raise KeyError('grandeza_id')
        sensor_id = request.GET.get('sensor')
        if(sensor_id == None):
            raise KeyError('sensor_id')
        minDate = request.GET.get('minDate')
        if(minDate == None):
            raise KeyError('minDate')
        maxDate = request.GET.get('maxDate')
        if(maxDate == None):
            raise KeyError('maxDate')
    except KeyError as e:
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})
    try:        
        leituras = Leitura.objects.filter(ambiente_id=ambiente_id,grandeza_id=grandeza_id,sensor_id=sensor_id,createdAt__range=(minDate, maxDate))
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})
    
    saidaLeituras = {}
    saidaLeituras['createdAt'] = []
    saidaLeituras['valores'] = []

    for leitura in leituras:
        saidaLeituras['createdAt'].append(str(leitura.createdAt))
        saidaLeituras['valores'].append(leitura.valor)

    saida = {}
    saida['sensor'] = str(Sensor.objects.get(uid=sensor_id))
    saida['grandeza'] = str(Grandeza.objects.get(codigo=grandeza_id))
    saida['ambiente'] = str(Ambiente.objects.get(uid=ambiente_id))
    saida['leituras'] = saidaLeituras

    return HttpResponse(
                json.dumps(saida),
                content_type='application/json; charset=utf8'
                )
