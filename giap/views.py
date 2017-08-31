# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from giap.forms import formaddcliente, formaddcentral, formsetcentral

# Create your views here.

def default(request):
    return render(request, 'default.html',)


def addcliente(request):
    formadd = formaddcliente()
    return render(request, 'addcliente.html',{'formadd': formadd,})

def addcooperativa(request):
    if request.method == 'POST':
        fosetcentral = formsetcentral(request.POST)
        if fosetcentral.is_valid():
            fosetcentral.save()
        fosetcentral = formsetcentral()
        return render(request, 'addcooperativa.html',
        {
            'fosetcentral': fosetcentral, 
        })

    fosetcentral = formsetcentral()
    return render(request, 'addcooperativa.html',
    {
        'fosetcentral': fosetcentral, 
        })
