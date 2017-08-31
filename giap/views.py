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
        foaddcentral = formaddcentral(request.POST)
        if foaddcentral.is_valid():
            foaddcentral.save
        foaddcentral = formaddcentral()
        fosetcentral = formsetcentral()
        return render(request, 'addcooperativa.html',
        {
            'foaddcentral': foaddcentral,
            'fosetcentral': fosetcentral, 
        })

    foaddcentral = formaddcentral()
    fosetcentral = formsetcentral()
    return render(request, 'addcooperativa.html',
    {
        'foaddcentral': foaddcentral,
        'fosetcentral': fosetcentral, 
        })
