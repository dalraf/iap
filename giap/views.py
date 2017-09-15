# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.forms import modelformset_factory

from giap.forms import formcentral, formcooperativa, formpa, formcliente, formtransacao, pesquisa

from giap.models import central, cooperativa, pa, cliente, transacao

from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required

from collections import OrderedDict

# Create your views here.

# Funcao edit add

class savefilter(object):
    def __init__(self, form):
        pass
    saida = True
    mensagem = ""


def editadd(request, id, modelo, formmodel, templateedit, urlretorno, savefilter=savefilter):
    if request.method == 'POST':
        if 'Salvar' in request.POST:
            if request.session['id'] == 'new':
                form = formmodel(request.POST)
                if form.is_valid():
                    resultfilter = savefilter(form)
                    if resultfilter.saida:
                        inst = form.save(commit=False)
                        inst.usuario = request.user.username
                        inst.save()
                        return redirect(urlretorno)
                    else:
                        request.session['confirmadelecao'] = 'Não'
                        mensagem = resultfilter.mensagem
                        textoformato = 'text-info'
                        return render(request, templateedit,{
                        'form': form,
                        'urlretorno': urlretorno,
                        }) 
                else:
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Adicionado'
                    textoformato = 'text-info'
                    return render(request, templateedit,{
                    'form': form,
                    'urlretorno': urlretorno,
                    })               
            else:
                modeloinstance = modelo.objects.get(id=request.session['id'])
                form = formmodel(request.POST, instance=modeloinstance)
                if form.is_valid():
                    inst = form.save(commit=False)
                    inst.usuario = request.user.username
                    inst.save()
                    return redirect(urlretorno)
                else:
                    request.session['confirmadelecao'] = 'Não'
                    mensagem = 'Registro Atualizado'
                    textoformato = 'text-info'
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

# View default
@login_required
def default(request):
    return render(request, 'default.html',)

# View Central
@login_required
def editaddcentral(request, id=None):
    return editadd(request,id,central,formcentral,'editadd.html','listarcentral')

@login_required
def listarcentral(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcentral'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(central.objects.filter(sigla_central__contains=filtro).values())
    else:
        form = pesquisa()
        listaget = list(central.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[central._meta.get_field('sigla_central').verbose_name] = i['sigla_central']
        j[central._meta.get_field('numcentral').verbose_name] = i['numcentral']
        j[central._meta.get_field('data').verbose_name] = i['data']
        lista.append(j)
    return render(request,templatelist, {'form': form,'editurl': editurl,'lista': lista})

# View cooperativa
@login_required
def editaddcooperativa(request, id=None):
    return editadd(request,id,cooperativa,formcooperativa,'editadd.html','listarcooperativa')

@login_required
def listarcooperativa(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcooperativa'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(cooperativa.objects.filter(sigla_cooperativa__contains=filtro).values())
    else:
        form = pesquisa()
        listaget = list(cooperativa.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[cooperativa._meta.get_field('sigla_cooperativa').verbose_name] = i['sigla_cooperativa']
        j[cooperativa._meta.get_field('numcooperativa').verbose_name] = i['numcooperativa']
        j[cooperativa._meta.get_field('data').verbose_name] = i['data']
        idcentral = i['central_id']
        j['Central'] = central.objects.get(id=idcentral).sigla_central

        lista.append(j)        
    return render(request,templatelist, {'form': form,'editurl': editurl,'lista': lista})

# View PA
@login_required
def editaddpa(request, id=None):
    return editadd(request,id,pa,formpa,'editadd.html','listarpa')

@login_required
def listarpa(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddpa'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(pa.objects.filter(sigla_pa__contains=filtro).values())
    else:
        form = pesquisa()
        listaget = list(pa.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[pa._meta.get_field('sigla_pa').verbose_name] = i['sigla_pa']
        j[pa._meta.get_field('numpa').verbose_name] = i['numpa']
        idcooperativa = i['cooperativa_id']
        j['Cooperativa'] = cooperativa.objects.get(id=idcooperativa).sigla_cooperativa
        j[pa._meta.get_field('data').verbose_name] = i['data']
        lista.append(j)        
    return render(request,templatelist, {'form': form, 'editurl': editurl,'lista': lista})

# View Cliente
@login_required
def editaddcliente(request, id=None):
    return editadd(request,id,cliente,formcliente,'editadd.html','listarcliente')

@login_required
def listarcliente(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcliente'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(cliente.objects.filter(nome_cliente__contains=filtro).values())
    else:
        form = pesquisa()
        listaget = list(cliente.objects.all().values())
    tipodepessoadict = dict(cliente._meta.get_field('tipodepessoa').flatchoices)
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[cliente._meta.get_field('nome_cliente').verbose_name] = i['nome_cliente']
        j[cliente._meta.get_field('numcpfcpnj').verbose_name] = i['numcpfcpnj']
        j[cliente._meta.get_field('tipodepessoa').verbose_name] = tipodepessoadict[i['tipodepessoa']]
        idpa = i['pa_id']
        j[cliente._meta.get_field('pa').verbose_name] = pa.objects.get(id=idpa).sigla_pa
        lista.append(j)        
    return render(request,templatelist, {'form': form, 'editurl': editurl,'lista': lista})

# View transacao
@login_required
def editaddtransacao(request, id=None):
    class savefilter(object):
        def __init__(self, form):
            if transacao.objects.filter(produto=form.cleaned_data['produto']).count  > 0:
                self.saida = False
                self.mensagem = "Produto já existe"
            else:
                self.saida = True
                self.mensagem = ""

    return editadd(request,id,transacao,formtransacao,'editadd.html','listartransacao',savefilter)

@login_required
def listartransacao(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddtransacao'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(transacao.objects.filter(cliente__nome_cliente__contains=filtro).values())
    else:
        form = pesquisa()
        listaget = list(transacao.objects.all().values())
    produtodict = dict(transacao._meta.get_field('produto').flatchoices)
    grupodict = dict(transacao._meta.get_field('grupo').flatchoices)
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        idcliente = i['cliente_id']
        j[transacao._meta.get_field('cliente').verbose_name] = cliente.objects.get(id=idcliente).nome_cliente
        j[transacao._meta.get_field('produto').verbose_name] = produtodict[i['produto']]
        j[transacao._meta.get_field('grupo').verbose_name] = grupodict[i['grupo']]
        j[transacao._meta.get_field('usuario').verbose_name] = i['usuario']
        j[transacao._meta.get_field('data').verbose_name] = i['data']
        lista.append(j)        
    return render(request,templatelist, {'form': form, 'editurl': editurl,'lista': lista})