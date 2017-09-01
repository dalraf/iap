# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from giap.forms import formcentral

from giap.models import central

from django.views.generic.edit import FormView

# Create your views here.

def default(request):
    return render(request, 'default.html',)

def editaddcentral(request):
    if request.method == 'POST':
        form = formcentral(request.POST)
        if form.is_valid():
                form.save()
        form = formcentral()
        return redirect('listarcentral',)
    
    form = formcentral()
    return render(request, 'editaddcentral.html',
    {
        'form': form,
        })


def listarcentral(request):
    centrallist = central.objects.all()
    return render(request,'listarcentral.html', {'centrallist': centrallist})
