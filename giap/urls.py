from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^listarcentral/$', views.listarcentral, name='listarcentral'),
    url(r'^editaddcentral/(?P<id>[0-9]+|new)/$', views.editaddcentral, name='editaddcentral'),
    url(r'^listarcooperativa/$', views.listarcooperativa, name='listarcooperativa'),
    url(r'^editaddcooperativa/(?P<id>[0-9]+|new)/$', views.editaddcooperativa, name='editaddcooperativa'),
    url(r'^listarpa/$', views.listarpa, name='listarpa'),
    url(r'^editaddpa/(?P<id>[0-9]+|new)/$', views.editaddpa, name='editaddpa'),
]