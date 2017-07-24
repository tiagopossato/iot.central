from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from . import models
from interface.decorators import ajax_login_required

# Create your views here.
@login_required(login_url='/login')
def mqtt_status(request):
    try:
        m = models.Mqtt.objects.get()
    except models.Mqtt.DoesNotExist:
        m = None
    return render(request, 'comunicacao/mqtt.html', {
        'mqtt_descricao': m.descricao if m != None else '', 
        'mqtt_status': m.status if m != None else 0, 
        'mqtt_servidor': m.servidor if m != None else ''
    })

# @ajax_login_required
# @method_decorator(csrf_exempt, name='dispatch')
def get_centrais_inativas(request):
    print("aqui veio!")
    return HttpResponse({'um':1}, mimetype='application/json')
