from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login', views.login_view),
    url(r'^logout', views.logout_view),
    url(r'^$', views.index),
]