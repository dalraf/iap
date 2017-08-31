# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from giap.forms import formaddcliente, formaddcooperativa, formaddcentral, formaddpa

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
        foaddcoop = formaddcooperativa(request.POST)
        if foaddcoop.is_valid():
            foaddcoop.save
        foaddpa = formaddpa(request.POST)
        if foaddpa.is_valid():
            foaddpa.save
        foaddcentral = formaddcentral()
        foaddcoop = formaddcooperativa()
        foaddpa = formaddpa()
        return render(request, 'addcooperativa.html',
        {
            'foaddcentral': foaddcentral, 
            'foaddcoop': foaddcoop,
            'foaddpa': foaddpa,
        })

    foaddcentral = formaddcentral()
    foaddcoop = formaddcooperativa()
    foaddpa = formaddpa()
    return render(request, 'addcooperativa.html',
    {
        'foaddcentral': foaddcentral, 
        'foaddcoop': foaddcoop,
        'foaddpa': foaddpa,
        })
