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
        print("----grandezasLidas-----")
        antes = datetime.utcnow()
        grandezasLidas = Leitura.objects.filter(ambiente_id=id).only('grandeza').values('grandeza').distinct()
        print(datetime.utcnow()-antes)
        
        grandezas = []
        for g in grandezasLidas:
            print("----grandeza-----")
            antes = datetime.utcnow()
            grandeza = Grandeza.objects.get(codigo=g['grandeza'])
            print(datetime.utcnow()-antes)
            
            print("----sensoresLidos-----")
            antes = datetime.utcnow()
            sensoresLidos = Leitura.objects.filter(ambiente_id=id, grandeza_id=grandeza.codigo).only('sensor').values('sensor').distinct()
            print(datetime.utcnow()-antes)
            
            sensores = []
            for s in sensoresLidos:
                print("----sensorLeituras-----")
                antes = datetime.utcnow()
                sensor = Sensor.objects.get(uid=s['sensor'])
                print(datetime.utcnow()-antes)
                
                # print("----sensorLeituras-----")
                # antes = datetime.utcnow()
                # sensorLeituras = Leitura.objects.filter(ambiente_id=id, grandeza_id=grandeza.codigo, sensor=sensor).only('createdAt')
                # print(datetime.utcnow()-antes)
                
                # print("----maxDate-----")
                # antes = datetime.utcnow()
                # maxDate = Leitura.objects.filter(ambiente_id=id, grandeza_id=grandeza.codigo, sensor=sensor).aggregate(Max('createdAt'))
                # print(datetime.utcnow()-antes)
                # print("----minDate-----")
                # antes = datetime.utcnow()
                # minDate = Leitura.objects.filter(ambiente_id=id, grandeza_id=grandeza.codigo, sensor=sensor).aggregate(Min('createdAt'))
                # print(datetime.utcnow()-antes)
                sensores.append({'uid':sensor.uid,
                                'descricao':sensor.descricao, 
                                # 'maxDate':maxDate['createdAt__max'],
                                # 'minDate':minDate['createdAt__min']
                                })
            grandezas.append({'codigo':grandeza.codigo, 'nome':grandeza.nome, 'sensores':sensores})

    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})
    
    try:
        return JsonResponse(status=200, data=grandezas, safe=False)
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})

@ajax_login_required
def daterange(request):
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
    except KeyError as e:
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})

    try:
        print("----maxDate-----")
        antes = datetime.utcnow()
        maxDate = Leitura.objects.filter(ambiente_id=ambiente_id, grandeza_id=grandeza_id, sensor=sensor_id).aggregate(Max('createdAt'))
        print(datetime.utcnow()-antes)
        print("----minDate-----")
        antes = datetime.utcnow()
        minDate = Leitura.objects.filter(ambiente_id=ambiente_id, grandeza_id=grandeza_id, sensor=sensor_id).aggregate(Min('createdAt'))
        print(datetime.utcnow()-antes)
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})
    
    try:
        return JsonResponse(status=200, data={'maxDate':maxDate['createdAt__max'],'minDate':minDate['createdAt__min']}, safe=False)
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
