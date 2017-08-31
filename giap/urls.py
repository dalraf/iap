from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^addclient/$', views.addcliente, name='addcliente'),
]