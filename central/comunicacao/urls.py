from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.mqtt_status),
    url(r'^mqtt-config', views.mqtt_config),
    url(r'^centrais-inativas', views.get_centrais_inativas)
]