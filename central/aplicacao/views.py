from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from interface.decorators import ajax_login_required
from datetime import datetime, timedelta, time
from aplicacao.models import Ambiente, Sensor, Grandeza, SensorGrandeza, Leitura
import json

@login_required(login_url='/login')
def leituras(request):
    print(datetime.now())
    leituras = Leitura.objects.filter(createdAt__date__gt=(datetime.now().date() - timedelta(days=1)))
    # ambientes = leituras.values('ambiente').distinct()
    # grandezas = leituras.values('grandeza').distinct()
    sensores = leituras.values('sensor').distinct()

    saida = []
    for s in sensores:
        ss = {}        
        sen = Sensor.objects.get(uid=s['sensor'])
        ss['descricao'] = sen.descricao
        ss['ambiente'] = sen.ambiente.nome
        ss['grandezas'] = []        
        sgs = SensorGrandeza.objects.filter(sensor=sen)
        for g in sgs:
            gg = {}
            gg['nome'] = g.grandeza.nome
            gg['unidade'] = g.grandeza.unidade
            gg['leituras'] = []
            try:
                for l in leituras.filter(ambiente=sen.ambiente, sensor=sen, grandeza=g.grandeza):
                    k = {}
                    k['valor'] = l.valor
                    k['createdAt'] = str(l.createdAt)
                    gg['leituras'].append(k)
            except Exception as e:
                print(e)
            ss['grandezas'].append(gg)
        
        saida.append(ss)

    # for a in ambientes:
    #     amb = Ambiente.objects.get(uid=a['ambiente'])
    #     ambiente = {}
    #     ambiente['uid'] = str(amb.uid)
    #     ambiente['nome'] = amb.nome
    #     ambiente['sensores'] = []
    #     # Montar lista de sensores e adicionar

    #     ambiente['sensores'].append({})
        
    #     leituras.append(ambiente)

    # for l in Leitura.objects.filter(createdAt__date__gt=(datetime.now().date() - timedelta(days=1))):
    #     s = {}
    #     s['valor'] = l.valor
    #     s['createdAt'] = str(l.createdAt)
    #     s['ambiente'] = str(l.ambiente.uid)
    #     s['sensor'] = str(l.sensor.uid)
    #     s['grandeza'] = l.grandeza.codigo
    #     leituras.append(s)
    print(datetime.now())
    return HttpResponse(
                json.dumps(saida),
                content_type='application/json; charset=utf8'
                )
