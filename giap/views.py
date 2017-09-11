# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.forms import modelformset_factory

from giap.forms import formcentral, formcooperativa, formpa, formcliente, formtransacao

from giap.models import central, cooperativa, pa, cliente, transacao

from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required

# Create your views here.

def editadd(request, id, modelo, formmodel, templateedit, urlretorno):
    if request.method == 'POST':
        form = formmodel(request.POST)
        if 'Salvar' in request.POST:
            if form.is_valid():
                if request.session['id'] == 'new':
                    inst = form.save(commit=False)
                    inst.usuario = request.user.username
                    inst.save()               
                    request.session['id'] = inst.id
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Adicionado'
                    textoformato = 'text-info'
                else:
                    inst = form.save(commit=False)
                    inst.id = request.session['id']
                    inst.usuario = request.user.username
                    inst.save()
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Atualizado'
                    textoformato = 'text-info'
                return redirect(urlretorno)
            else:
                return render(request, templateedit,{
                'form': form,
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
                objeto = get_object_or_404(modelo, id=request.session['id'])
                form = formmodel(instance=objeto)
                return render(request, templateedit,{
                'form': form,
                'mensagem': mensagem,
                'textoformato': textoformato,
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

@login_required
def default(request):
    return render(request, 'default.html',)

@login_required
def editaddcentral(request, id=None):
    return editadd(request,id,central,formcentral,'editadd.html','listarcentral')

@login_required
def listarcentral(request):
    templatelist = 'lista.html'
    editurl = 'editaddcentral'
    listaget = list(central.objects.all().values())
    lista = []
    for i in listaget:
        j = {}
        for key, value in i.iteritems():
            j[central._meta.get_field(key).verbose_name] = value
        lista.append(j)
    return render(request,templatelist, {'editurl': editurl,'lista': lista})

@login_required
def editaddcooperativa(request, id=None):
    return editadd(request,id,cooperativa,formcooperativa,'editadd.html','listarcooperativa')

@login_required
def listarcooperativa(request):
    templatelist = 'lista.html'
    editurl = 'editaddcooperativa'
    listaget = list(cooperativa.objects.all().values())
    lista = []
    for i in listaget:
        j = {}
        for key, value in i.iteritems():
            j[cooperativa._meta.get_field(key).verbose_name] = value
        idcentral = i['central_id']
        j['Central'] = central.objects.get(id=idcentral).sigla_central

        lista.append(j)        
    return render(request,templatelist, {'editurl': editurl,'lista': lista})

@login_required
def editaddpa(request, id=None):
    return editadd(request,id,pa,formpa,'editadd.html','listarpa')

@login_required
def listarpa(request):
    templatelist = 'lista.html'
    editurl = 'editaddpa'
    listaget = list(pa.objects.all().values())
    lista = []
    for i in listaget:
        j = {}
        for key, value in i.iteritems():
            j[pa._meta.get_field(key).verbose_name] = value
        idcooperativa = i['cooperativa_id']
        j['Cooperativa'] = cooperativa.objects.get(id=idcooperativa).sigla_cooperativa
        lista.append(j)        
    return render(request,templatelist, {'editurl': editurl,'lista': lista})

@login_required
def editaddcliente(request, id=None):
    return editadd(request,id,cliente,formcliente,'editadd.html','listarcliente')

@login_required
def listarcliente(request):
    templatelist = 'lista.html'
    editurl = 'editaddcliente'
    listaget = list(cliente.objects.all().values())
    tipodepessoadict = dict(cliente._meta.get_field('tipodepessoa').flatchoices)
    lista = []
    for i in listaget:
        j = {}
        for key, value in i.iteritems():
            j[cliente._meta.get_field(key).verbose_name] = value
        idpa = i['pa_id']
        j['Cooperativa/PA'] = pa.objects.get(id=idpa).sigla_pa
        j['Tipo de Pessoa'] = tipodepessoadict[i['tipodepessoa']]
        lista.append(j)        
    return render(request,templatelist, {'editurl': editurl,'lista': lista})


@login_required
def editaddtransacao(request, id=None):
    return editadd(request,id,transacao,formtransacao,'editadd.html','listartransacao')

@login_required
def listartransacao(request):
    templatelist = 'lista.html'
    editurl = 'editaddtransacao'
    listaget = list(transacao.objects.all().values())
    produtodict = dict(transacao._meta.get_field('produto').flatchoices)
    grupodict = dict(transacao._meta.get_field('grupo').flatchoices)
    lista = []
    for i in listaget:
        j = {}
        for key, value in i.iteritems():
            j[transacao._meta.get_field(key).verbose_name] = value
        idcliente = i['cliente_id']
        j['Cliente'] = cliente.objects.get(id=idcliente).nome_cliente
        j['Produto'] = produtodict[i['produto']]
        j['Grupo'] = grupodict[i['grupo']]
        lista.append(j)        
    return render(request,templatelist, {'editurl': editurl,'lista': lista})