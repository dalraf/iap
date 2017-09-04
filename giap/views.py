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
                if request.session['id'] == 'new':
                    novoreg = form.save()                
                    request.session['id'] = novoreg.id
                    mensagem = 'Registro Adicionado'   
                else:
                    inst = form.save(commit=False)
                    inst.id = request.session['id']
                    inst.save()
                    mensagem = 'Registro Atualizado'
                return render(request, 'editaddcentral.html',{
                    'form': form,
                    'mensagem' : mensagem,
                    })
            elif 'Deletar' in request.POST:
                if request.session['confirmadelecao'] == 'Sim':
                    central.objects.filter(id=request.session['id']).delete()
                    request.session['id'] == ''
                    request.session['confirmadelecao'] = 'Não'
                    return redirect('listarcentral',)
                else:
                    request.session['confirmadelecao'] = 'Sim'
                    mensagem = 'Confirma deleção?'
                    return render(request, 'editaddcentral.html',{
                    'form': form,
                    'mensagem': mensagem,
                    })
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
            request.session['confirmadelecao'] = 'Não'     
        return render(request, 'editaddcentral.html',
        {
            'id': id,
            'form': form,
            })


def listarcentral(request):
    centrallist = modelformset_factory(central, fields=("sigla_central", "numcentral", "id"), extra=0)
    return render(request,'listarcentral.html', {'centrallist': centrallist})
