from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
from comunicacao.models import Mqtt
from interface.decorators import ajax_login_required

@login_required(login_url='/login')
def mqtt_status(request):
    try:
        m = Mqtt.objects.get()
    except Mqtt.DoesNotExist:
        m = None
    return render(request, 'comunicacao/mqtt.html', {
        'mqtt_identificador': m.identificador if m != None else '',
        'mqtt_descricao': m.descricao if m != None else '',
        'mqtt_status': m.status if m != None else 0,
        'mqtt_servidor': m.servidor if m != None else ''
    })

@login_required(login_url='/login')
def mqtt_config(request):
    if(request.method != 'POST'):
        return HttpResponseNotAllowed(['POST'])
    try:
        username = request.POST.get('md-mqtt-username')
        if(username == None):
            raise KeyError('username')
        password = request.POST.get('md-mqtt-password')
        if(password == None):
            raise KeyError('password')
        servidor = request.POST.get('md-mqtt-servidor')
        if(servidor == None):
            raise KeyError('servidor')
        descricao = request.POST.get('md-mqtt-descricao')
        if(descricao == None):
            raise KeyError('descricao')
        identificador = request.POST.get('md-mqtt-identificador')
        if(identificador == None):
            raise KeyError('identificador')

        if(identificador == ''):
            print('identificador vazio, configurar nova central')
            try:
                m = Mqtt.objects.get()
                # Já existe uma configuração. ERRO
                return JsonResponse(status=400, data={'erro': 'Erro catastrófico, entre em contato com o fornecedor'})
            except Mqtt.DoesNotExist:
                try:
                    payload = {
                        'username': username,
                        'password': password,
                        'descricao': descricao
                    }
                    r = requests.post(servidor+'/central/nova', data=payload)
                    if(r.status_code == 200):
                        dados = r.json()
                        try:
                            if(dados['erro']):
                                print(dados['erro'])
                                return JsonResponse(status=400, data=dados, safe=False)
                        except Exception as e:
                            print('ok')
                        # Prossegue com o salvamento da central
                        config = Mqtt(identificador=dados['id'], status=1, descricao=dados['descricao'], servidor=servidor, keyFile=dados['keyFile'], certFile=dados['certFile'])
                        config.save()
                    else:
                        return JsonResponse(status=400, data={'erro': r.status_code})
                except requests.exceptions.ConnectionError as e:
                    return JsonResponse(status=400, data={'erro': 'Erro na conexão com o servidor'})
                except Exception as e:
                    return JsonResponse(status=400, data={'erro': str(e)})
        else:
            # TODO: Chama método para alterar dados da central no servidor
            try:
                config = Mqtt.objects.get()
                print(config)
                return JsonResponse(status=400, data={'erro': "Alteracao de dados ainda nao implementado"})
            except Mqtt.DoesNotExist:
                return JsonResponse(status=400, data={'erro': 'Erro catastrófico, entre em contato com o fornecedor'})            

        return redirect('/comunicacao')
    except KeyError as e:
        print('KeyError:' + str(e))
        return redirect('/comunicacao')


@ajax_login_required
def get_centrais_inativas(request):
    if(request.method != 'GET'):
        return HttpResponseNotAllowed(['GET'])
    if(request.is_ajax() == False):
        return JsonResponse(status=400, data={'erro': "Somente requisicoes AJAX!"})
    try:
        username = request.GET.get('username')
        if(username == None):
            raise KeyError('username')
        password = request.GET.get('password')
        if(password == None):
            raise KeyError('password')
        servidor = request.GET.get('servidor')
        if(servidor == None):
            raise KeyError('servidor')
    except KeyError as e:
        print(e)
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})

    try:
        payload = {
            'username': username,
            'password': password
        }
        r = requests.get(servidor+'/central/inativas', params=payload)
        if(r.status_code == 200):
            return JsonResponse(data=r.json(), safe=False)
        else:
            return JsonResponse(status=400, data={'erro': r.status_code})
    except requests.exceptions.ConnectionError as e:
        return JsonResponse(status=400, data={'erro': 'Erro na conexão com o servidor'})
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})


@ajax_login_required
def inativar_central(request):
    if(request.method != 'GET'):
        return HttpResponseNotAllowed(['GET'])
    if(request.is_ajax() == False):
        return JsonResponse(status=400, data={'erro': "Somente requisicoes AJAX!"})
    try:
        username = request.GET.get('username')
        if(username == None):
            raise KeyError('username')
        password = request.GET.get('password')
        if(password == None):
            raise KeyError('password')
    except KeyError as e:
        print(e)
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})
    
    try:
        config = None
        try:
            config = Mqtt.objects.get()
        except Mqtt.DoesNotExist:
            return JsonResponse(status=400, data={'erro': "Não existe configuração na central"})

        payload = {
            'username': username,
            'password': password
        }
        r = requests.post(config.servidor+'/central/' + str(config.identificador) + '/inativar', data=payload)
        if(r.status_code == 200):
            dados = r.json()
            try:
                if(dados['erro']):
                    print(dados['erro'])
                    return JsonResponse(status=400, data=dados, safe=False)
            except Exception as e:
                print('ok')
            # Apaga as configurações da central
            Mqtt.objects.all().delete()   
            return JsonResponse(status=200, data={});
        if(r.status_code == 404):
            return JsonResponse(status=400, data={'erro': 'Servidor não encontrado'})
        else:
            return JsonResponse(status=400, data={'erro': r.status_code})
    except requests.exceptions.ConnectionError as e:
        return JsonResponse(status=400, data={'erro': 'Erro na conexão com o servidor'})
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})


@ajax_login_required
@method_decorator(csrf_exempt, name='dispatch')
def reativar_central(request):

    if(request.method != 'POST'):
        return HttpResponseNotAllowed(['POST'])
    if(request.is_ajax() == False):
        return JsonResponse(status=400, data={'erro': "Somente requisicoes AJAX!"})
    try:
        username = request.POST.get('username')
        if(username == None):
            raise KeyError('username')

        password = request.POST.get('password')
        if(password == None):
            raise KeyError('password')

        servidor = request.POST.get('servidor')        
        if(servidor == None):
            raise KeyError('servidor')

        id = request.POST.get('id')
        if(id == None):
            raise KeyError('id')

    except KeyError as e:
        print(e)
        return JsonResponse(status=400, data={'erro': "Parâmetro " + str(e) + " não recebido"})

    try:
        payload = {
            'username': username,
            'password': password
        }
        r = requests.post(servidor+'/central/' + id + '/reativar', data=payload)
        if(r.status_code == 200):
            dados = r.json()
            try:
                if(dados['erro']):
                    print(dados['erro'])
                    return JsonResponse(status=400, data=dados, safe=False)
            except Exception as e:
                print('ok')
            # Prossegue com o salvamento da central
            config = Mqtt(identificador=dados['id'], status=1, descricao=dados['descricao'], servidor=servidor, keyFile=dados['keyFile'], certFile=dados['certFile'])
            config.save()
            return JsonResponse(status=200, data={});
        else:
            return JsonResponse(status=400, data={'erro': r.status_code})
    except requests.exceptions.ConnectionError as e:
        return JsonResponse(status=400, data={'erro': 'Erro na conexão com o servidor'})
    except Exception as e:
        return JsonResponse(status=400, data={'erro': str(e)})