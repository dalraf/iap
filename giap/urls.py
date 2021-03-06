from django.conf.urls import url
from django.contrib import admin
from giap.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', default, name='default'),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'} ,name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/giap'}, name='logout'),
    url(r'^listarcentral/$', listarcentral, name='listarcentral'),
    url(r'^editaddcentral/(?P<id>[0-9]+|new)/$', editaddcentral, name='editaddcentral'),
    url(r'^listarcooperativa/$', listarcooperativa, name='listarcooperativa'),
    url(r'^editaddcooperativa/(?P<id>[0-9]+|new)/$', editaddcooperativa, name='editaddcooperativa'),
    url(r'^listarpa/$', listarpa, name='listarpa'),
    url(r'^editaddpa/(?P<id>[0-9]+|new)/$', editaddpa, name='editaddpa'),
    url(r'^listarcliente/$', listarcliente, name='listarcliente'),
    url(r'^editaddcliente/(?P<id>[0-9]+|new)/$', editaddcliente, name='editaddcliente'),
    url(r'^listartransacao/$', listartransacao, name='listartransacao'),
    url(r'^editaddtransacao/(?P<id>[0-9]+|new)/$', editaddtransacao, name='editaddtransacao'),
    url(r'^editaddsisbrcsv/(?P<id>[0-9]+|new)/$', editaddsisbrcsv, name='editaddsisbrcsv'),
    url(r'^listarsisbrcsv/$', listarsisbrcsv, name='listarsisbrcsv'),
    url(r'^sisbrprocessalist/$', sisbrprocessalist.as_view(), name='sisbrprocessalist'),
    url(r'^addtransacao/(?P<cliente>[0-9]+)/(?P<produto>[0-9]+)/$', addtransacao.as_view(), name='addtransacao'),
    url(r'^addcliente/(?P<numcpfcnpj>[0-9.-]+)/$', addcliente.as_view(), name='addcliente'),
]