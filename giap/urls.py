from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^listarcentral/$', views.listarcentral, name='listarcentral'),
    url(r'^editaddcentral/(?P<id>[0-9]+|new)/$', views.editaddcentral, name='editaddcentral'),
    url(r'^deletarcentral/(?P<id>[0-9]+)/$', views.deletarcentral, name='deletarcentral'),
]