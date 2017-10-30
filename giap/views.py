# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, redirect, render, reverse

from django.core.urlresolvers import reverse_lazy

from django.forms import modelformset_factory

from giap.forms import formcentral, formcooperativa, formpa, formcliente, formtransacao, pesquisa, formsisbrcsv, formprocessarsisbr

from giap.models import central, cooperativa, pa, cliente, transacao, sisbrcsv, sisbrprocessa

from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required, permission_required

from django.utils.decorators import method_decorator

from collections import OrderedDict

from django.utils import timezone

import datetime

from django.db.models import Q

from django.views.generic.list import ListView

from django.views.generic.edit import CreateView

from django.conf import settings

import csv

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
                form = formmodel(request.POST, request.FILES)
                if form.is_valid():
                    resultfilter = savefilter(form)
                    if resultfilter.saida:
                        inst = form.save(commit=False)
                        inst.usuario = request.user.username
                        inst.save()
                        return redirect(urlretorno)
                    else:
                        request.session['confirmadelecao'] = False
                        mensagem = resultfilter.mensagem
                        textoformato = 'text-danger'
                        return render(request, templateedit, {
                            'form': form,
                            'textoformato': textoformato,
                            'urlretorno': urlretorno,
                            'mensagem': mensagem,
                        })
                else:
                    request.session['confirmadelecao'] = False
                    mensagem = 'Registro Adicionado'
                    textoformato = 'text-info'
                    return render(request, templateedit, {
                        'form': form,
                        'urlretorno': urlretorno,
                    })
            else:
                modeloinstance = modelo.objects.get(id=request.session['id'])
                form = formmodel(request.POST, request.FILES,
                                 instance=modeloinstance)
                if form.is_valid():
                    resultfilter = savefilter(form)
                    if resultfilter.saida:
                        inst = form.save(commit=False)
                        inst.usuario = request.user.username
                        inst.save()
                        return redirect(urlretorno)
                    else:
                        request.session['confirmadelecao'] = False
                        mensagem = resultfilter.mensagem
                        textoformato = 'text-danger'
                        return render(request, templateedit, {
                            'form': form,
                            'textoformato': textoformato,
                            'urlretorno': urlretorno,
                            'mensagem': mensagem,
                        })
                else:
                    request.session['confirmadelecao'] = False
                    mensagem = 'Registro Atualizado'
                    textoformato = 'text-info'
                    return render(request, templateedit, {
                        'form': form,
                        'urlretorno': urlretorno,
                    })
        elif 'Deletar' in request.POST:
            request.session['confirmadelecao'] = True
            mensagem = 'Confirma deleção?'
            textoformato = 'text-danger'
            objeto = get_object_or_404(modelo, id=request.session['id'])
            form = formmodel(instance=objeto)
            return render(request, templateedit, {
                'form': form,
                'mensagem': mensagem,
                'textoformato': textoformato,
                'urlretorno': urlretorno,
            })
        elif 'Confirmar' in request.POST:
            if request.session['confirmadelecao'] == True:
                modelo.objects.filter(id=request.session['id']).delete()
                request.session['id'] == ''
                request.session['confirmadelecao'] = False
                return redirect(urlretorno,)
        elif 'Cancelar' in request.POST:
            if request.session['confirmadelecao'] == True:
                request.session['confirmadelecao'] = False
                mensagem = 'Deleção cancelada'
                textoformato = 'text-info'
                objeto = get_object_or_404(modelo, id=request.session['id'])
                form = formmodel(instance=objeto)
                return render(request, templateedit, {
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
            request.session['confirmadelecao'] = False
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
@permission_required('giap.add_central', raise_exception=True)
@permission_required('giap.change_central', raise_exception=True)
@permission_required('giap.delete_central', raise_exception=True)
def editaddcentral(request, id=None):
    return editadd(request, id, central, formcentral, 'editadd.html', 'listarcentral')


@login_required
def listarcentral(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcentral'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(central.objects.filter(
                Q(sigla_central__contains=filtro) | Q(numcentral__contains=filtro)).values())
    else:
        form = pesquisa()
        listaget = list(central.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[central._meta.get_field(
            'sigla_central').verbose_name] = i['sigla_central']
        j[central._meta.get_field('numcentral').verbose_name] = i['numcentral']
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})

# View cooperativa


@login_required
@permission_required('giap.add_ccooperativa', raise_exception=True)
@permission_required('giap.change_cooperativa', raise_exception=True)
@permission_required('giap.delete_cooperativa', raise_exception=True)
def editaddcooperativa(request, id=None):
    return editadd(request, id, cooperativa, formcooperativa, 'editadd.html', 'listarcooperativa')


@login_required
def listarcooperativa(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcooperativa'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(cooperativa.objects.filter(
                Q(sigla_cooperativa__contains=filtro) | Q(numcooperativa__contains=filtro)).values())
    else:
        form = pesquisa()
        listaget = list(cooperativa.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[cooperativa._meta.get_field(
            'sigla_cooperativa').verbose_name] = i['sigla_cooperativa']
        j[cooperativa._meta.get_field(
            'numcooperativa').verbose_name] = i['numcooperativa']
        idcentral = i['central_id']
        j['Central'] = central.objects.get(id=idcentral).sigla_central
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})

# View PA


@login_required
@permission_required('giap.add_pa', raise_exception=True)
@permission_required('giap.change_pa', raise_exception=True)
@permission_required('giap.delete_pa', raise_exception=True)
def editaddpa(request, id=None):
    return editadd(request, id, pa, formpa, 'editadd.html', 'listarpa')


@login_required
def listarpa(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddpa'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(pa.objects.filter(Q(sigla_pa__contains=filtro) | Q(numpa__contains=filtro) | Q(
                cooperativa__sigla_cooperativa__contains=filtro) | Q(cooperativa__numcooperativa__contains=filtro)).values())
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
        j['Cooperativa'] = cooperativa.objects.get(
            id=idcooperativa).sigla_cooperativa
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})

# View Cliente


@login_required
@permission_required('giap.add_cliente', raise_exception=True)
@permission_required('giap.change_cliente', raise_exception=True)
@permission_required('giap.delete_cliente', raise_exception=True)
def editaddcliente(request, id=None):
    return editadd(request, id, cliente, formcliente, 'editadd.html', 'listarcliente',)


@login_required
def listarcliente(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddcliente'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(cliente.objects.filter(
                Q(nome_cliente__contains=filtro) | Q(numcpfcnpj__contains=filtro)).values())
    else:
        form = pesquisa()
        listaget = list(cliente.objects.all().values())
    tipodepessoadict = dict(
        cliente._meta.get_field('tipodepessoa').flatchoices)
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[cliente._meta.get_field(
            'nome_cliente').verbose_name] = i['nome_cliente']
        j[cliente._meta.get_field('numcpfcnpj').verbose_name] = i['numcpfcnpj']
        j[cliente._meta.get_field(
            'tipodepessoa').verbose_name] = tipodepessoadict[i['tipodepessoa']]
        idpa = i['pa_id']
        idcooperativa = pa.objects.get(id=idpa).cooperativa.id
        j[cliente._meta.get_field('pa').verbose_name] = str(pa.objects.get(
            id=idpa).sigla_pa) + "/" + str(cooperativa.objects.get(id=idcooperativa).sigla_cooperativa)
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})

# View transacao


@login_required
@permission_required('giap.add_transacao', raise_exception=True)
@permission_required('giap.change_transacao', raise_exception=True)
@permission_required('giap.delete_transacao', raise_exception=True)
def editaddtransacao(request, id=None):
    return editadd(request, id, transacao, formtransacao, 'editadd.html', 'listartransacao', savefilter)


@login_required
def listartransacao(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddtransacao'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(transacao.objects.filter(Q(cliente__nome_cliente__contains=filtro) | Q(
                cliente__numcpfcnpj__contains=filtro)).values())
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
        j[transacao._meta.get_field('cliente').verbose_name] = cliente.objects.get(
            id=idcliente).nome_cliente
        j[transacao._meta.get_field(
            'produto').verbose_name] = produtodict[i['produto']]
        j[transacao._meta.get_field(
            'grupo').verbose_name] = grupodict[i['grupo']]
        j['Dias para vencer'] = (i['vencimento'] - timezone.now().date()).days
        j[transacao._meta.get_field('usuario').verbose_name] = i['usuario']
        j[transacao._meta.get_field('data').verbose_name] = i['data']
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})


@login_required
@permission_required('giap.add_sisbrcsv', raise_exception=True)
@permission_required('giap.change_sisbrcsv', raise_exception=True)
@permission_required('giap.delete_sisbrcsv', raise_exception=True)
def editaddsisbrcsv(request, id=None):
    return editadd(request, id, sisbrcsv, formsisbrcsv, 'editadd.html', 'listarsisbrcsv', savefilter)


@login_required
def listarsisbrcsv(request):
    form = pesquisa()
    templatelist = 'lista.html'
    editurl = 'editaddsisbrcsv'
    if request.method == 'POST':
        form = pesquisa(request.POST)
        if form.is_valid():
            filtro = form.cleaned_data['filtro']
            listaget = list(sisbrcsv.objects.filter(
                Q(sisbrcsvfile__contains=filtro)).values())
    else:
        form = pesquisa()
        listaget = list(sisbrcsv.objects.all().values())
    lista = []
    for i in listaget:
        j = OrderedDict()
        j['id'] = i['id']
        j[sisbrcsv._meta.get_field(
            'datareferencia').verbose_name] = i['datareferencia']
        j[sisbrcsv._meta.get_field(
            'sisbrcsvfile').verbose_name] = i['sisbrcsvfile']
        lista.append(j)
    return render(request, templatelist, {'form': form, 'editurl': editurl, 'lista': lista})


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('giap.add_sisbrcsv', raise_exception=True),name='dispatch')
@method_decorator(permission_required('giap.change_sisbrcsv', raise_exception=True), name='dispatch')
@method_decorator(permission_required('giap.delete_sisbrcsv', raise_exception=True), name='dispatch')
class sisbrprocessalist(ListView):
    
    model = sisbrprocessa
    template_name = 'sisbrprocessalist.html'

    def get_queryset(self):
        if self.request.GET.get('sisbrcsv'):
            sisbrcsv_val = self.request.GET.get('sisbrcsv')
        else:
            sisbrcsv_val = sisbrcsv.objects.all().first()
        context = sisbrprocessa.objects.filter(sisbrcsv=sisbrcsv_val).order_by('numcpfcnpj')
        return context

    def get_context_data(self, **kwargs):
        context = super(sisbrprocessalist, self).get_context_data(**kwargs)
        if self.request.GET.get('filtro'):
            context['form'] = formprocessarsisbr(self.request.GET)
        else:
            context['form'] = formprocessarsisbr
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('giap.add_sisbrcsv', raise_exception=True),name='dispatch')
@method_decorator(permission_required('giap.change_sisbrcsv', raise_exception=True), name='dispatch')
@method_decorator(permission_required('giap.delete_sisbrcsv', raise_exception=True), name='dispatch')
class addtransacao(CreateView):
    model = transacao
    success_url=reverse_lazy('sisbrprocessalist')
    template_name = 'addtransacao.html'
    fields = ['cliente','produto','usuario','data','vencimento','grupo']
    def get_initial(self):
        initial = {}
        initial['cliente'] = self.kwargs['cliente']
        initial['produto'] = self.kwargs['produto']
        initial['usuario'] = self.request.user.username
        return initial

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('giap.add_sisbrcsv', raise_exception=True),name='dispatch')
@method_decorator(permission_required('giap.change_sisbrcsv', raise_exception=True), name='dispatch')
@method_decorator(permission_required('giap.delete_sisbrcsv', raise_exception=True), name='dispatch')
class addcliente(CreateView):
    model = cliente
    success_url=reverse_lazy('sisbrprocessalist')
    template_name = 'addtransacao.html'
    fields = ['pa','tipodepessoa','numcpfcnpj','nome_cliente','usuario']
    def get_initial(self):
        initial = {}
        initial['numcpfcnpj'] = self.kwargs['numcpfcnpj']
        initial['usuario'] = self.request.user.username
        return initial

    