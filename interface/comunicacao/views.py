from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.
@login_required(login_url='/login')
def mqtt_view(request):
    try:
        m = models.Mqtt.objects.get()
    except models.Mqtt.DoesNotExist:
        m = None
    return render(request, 'central/mqtt.html', {
        'mqtt_descricao': m.descricao if m != None else '', 
        'mqtt_status': m.status if m != None else 0, 
        'mqtt_servidor': m.servidor if m != None else ''
    })