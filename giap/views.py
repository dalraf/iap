# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.forms import modelformset_factory

from giap.forms import formcentral, formcooperativa

from giap.models import central, cooperativa

from django.views.generic.edit import FormView

# Create your views here.

def editadd(request, id, modelo, formmodel, templateedit, urlretorno):
    if request.method == 'POST':
        form = formmodel(request.POST)
        if form.is_valid():
            if 'Salvar' in request.POST:
                if request.session['id'] == 'new':
                    novoreg = form.save()                
                    request.session['id'] = novoreg.id
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Adicionado'
                    textoformato = 'text-info'
                else:
                    inst = form.save(commit=False)
                    inst.id = request.session['id']
                    inst.save()
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Atualizado'
                    textoformato = 'text-info'
                return render(request, templateedit,{
                    'form': form,
                    'mensagem' : mensagem,
                    'textoformato': textoformato,
                    'urlretorno': urlretorno,
                    })
            elif 'Deletar' in request.POST:
                if request.session['confirmadelecao'] == 'Sim':
                    modelo.objects.filter(id=request.session['id']).delete()
                    request.session['id'] == ''
                    request.session['confirmadelecao'] = 'Não'
                    return redirect(urlretorno,)
                else:
                    request.session['confirmadelecao'] = 'Sim'
                    mensagem = 'Confirma deleção?'
                    textoformato = 'text-danger'
                    return render(request, templateedit,{
                    'form': form,
                    'mensagem': mensagem,
                    'textoformato': textoformato,
                    'urlretorno': urlretorno,
                    })
        else:
            return render(request, templateedit,{
            'form': form,
            'urlretorno': urlretorno,
            })

 
    if request.method == 'GET' and id:
        if id == 'new':
            request.session['id'] = 'new'
            form = formmodel()
        else:
            objeto = get_object_or_404(modelo, id=id)
            form = formmodel(request.POST or None, instance=objeto)
            request.session['id'] = id
            request.session['confirmadelecao'] = 'Não'     
        return render(request, templateedit,
        {
            'id': id,
            'form': form,
            'urlretorno': urlretorno,
            })


def default(request):
    return render(request, 'default.html',)

def editaddcentral(request, id=None):
    return editadd(request,id,central,formcentral,'editadd.html','listarcentral')

def listarcentral(request):
    templatelist = 'lista.html'
    editurl = 'editaddcentral'
    formset = modelformset_factory(central, fields=("sigla_central", "numcentral"), extra=0)
    return render(request,templatelist, {'editurl': editurl,'formset': formset})

def editaddcooperativa(request, id=None):
    return editadd(request,id,cooperativa,formcooperativa,'editadd.html','listarcooperativa')

def listarcooperativa(request):
    templatelist = 'lista.html'
    editurl = 'editaddcooperativa'
    lista = list(cooperativa.objects.all().values())
    for i in lista:
        i['sigla_central'] = central.objects.get(id=i['central_id']).sigla_central

    #formset = modelformset_factory(cooperativa, fields=("sigla_cooperativa", "numcooperativa",), extra=0)
    return render(request,templatelist, {'editurl': editurl,'lista': lista})