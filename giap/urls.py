from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^editaddcentral/$', views.editaddcentral, name='editaddcentral'),
    url(r'^listarcentral/$', views.listarcentral, name='listarcentral'),
]