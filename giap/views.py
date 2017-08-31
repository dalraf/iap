# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from giap.forms import formaddcliente

# Create your views here.

def default(request):
    return render(request, 'default.html',)


def addcliente(request):
    formadd = formaddcliente()
    return render(request, 'addcliente.html',{'formadd': formadd,})