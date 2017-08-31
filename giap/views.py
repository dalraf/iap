# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def default(request):
    return render(request, 'default.html',)


def addcliente(request):
    return render(request, 'addcliente.html',)