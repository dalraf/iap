# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from giap.forms import formaddcliente, formaddcentral, formsetcentral

from giap.models import central

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
                foaddcentral.save()
        foaddcentral = formaddcentral()
        return render(request, 'addcooperativa.html',
        {
            'foaddcentral': foaddcentral,
        })
    
    foaddcentral = formaddcentral()
    return render(request, 'addcooperativa.html',
    {
        'foaddcentral': foaddcentral,
        })
