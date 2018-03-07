from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^grafico', views.grafico),
    url(r'^metadata', views.metadados),
    url(r'^leituras', views.leituras),
]