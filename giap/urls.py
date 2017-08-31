from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^addcliente/$', views.addcliente, name='addcliente'),
    url(r'^addcooperativa/$', views.addcooperativa, name='addcooperativa'),
]