# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from giap.forms import formcentral

from giap.models import central

from django.views.generic.edit import FormView

# Create your views here.

def default(request):
    return render(request, 'default.html',)

def editaddcentral(request, id=None):
    if request.method == 'POST':
        form = formcentral(request.POST)
        if form.is_valid():
            if request.session['id']:
                inst = form.save(commit=False)
                inst.id = request.session['id']
                inst.save()
            else:
                form.save()
        return redirect('listarcentral',)
    if id:
        if id == 'new':
            form = formcentral()
        else:
            objeto = get_object_or_404(central, id=id)
            form = formcentral(request.POST or None, instance=objeto)
            request.session['id'] = id       
    return render(request, 'editaddcentral.html',
    {
        'form': form,
        })


def listarcentral(request):
    centrallist = central.objects.all()
    return render(request,'listarcentral.html', {'centrallist': centrallist})
