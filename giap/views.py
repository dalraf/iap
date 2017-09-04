# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.forms import modelformset_factory

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
            if 'Salvar' in request.POST:
                if request.session['id'] != 'new':
                    inst = form.save(commit=False)
                    inst.id = request.session['id']
                    inst.save()
                else:
                    form.save()
                return render(request, 'editaddcentral.html',{
                    'form': form,
                    })
            elif 'Deletar' in request.POST:
                central.objects.filter(id=request.session['id']).delete()
                request.session['id'] == ''
                return redirect('listarcentral',)
            elif 'Voltar' in request.POST:
                request.session['id'] == ''
                return redirect('listarcentral',)
            else:
                return render(request, 'editaddcentral.html',{
                'form': form,
                })

 
    if request.method == 'GET' and id:
        if id == 'new':
            request.session['id'] = 'new'
            form = formcentral()
        else:
            objeto = get_object_or_404(central, id=id)
            form = formcentral(request.POST or None, instance=objeto)
            request.session['id'] = id       
        return render(request, 'editaddcentral.html',
        {
            'id': id,
            'form': form,
            })

def deletarcentral(request,id):
    central.objects.filter(id=id).delete()
    return redirect('listarcentral',)



def listarcentral(request):
    centrallist = modelformset_factory(central, fields=("sigla_central", "numcentral", "id"), extra=0)
    return render(request,'listarcentral.html', {'centrallist': centrallist})
