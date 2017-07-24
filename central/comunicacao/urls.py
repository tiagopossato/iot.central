from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mqtt_status),
    url(r'^centrais_inativas', views.get_centrais_inativas)
]