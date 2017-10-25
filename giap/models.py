# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils import timezone

from datetime import datetime, timedelta

from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

from pycpfcnpj import cpfcnpj

from django.db.models import Q

import uuid

import os

from django.conf import settings

import csv


def validate_cpfcpnj(value):
    if not cpfcnpj.validate(str(value)):
        raise ValidationError(
            _('%(value)s inválido (CPF/CNPJ Inválido)'),
            params={'value': value},
        )


def validate_vencimento(value):
    if value <= timezone.now().date():
        raise ValidationError(
            _('%(value)s inválido (Data inferior a data atual)'),
            params={'value': value},
        )


# Create your models here.

class central(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_central = models.CharField(
        'Nome', unique=True, help_text='Nome da Central', max_length=50,)
    numcentral = models.DecimalField(
        'Número', unique=True, help_text='Número da Central, máx. 4 dígitos', max_digits=4, decimal_places=0, )
    usuario = models.CharField('Usuario', max_length=150,)
    data = models.DateTimeField(
        'Data e Hora de inclusão', default=timezone.now)

    def __unicode__(self):
        return self.sigla_central


class cooperativa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_cooperativa = models.CharField(
        'Nome', unique=True, help_text='Nome da Cooperativa', max_length=50,)
    numcooperativa = models.DecimalField(
        'Número', unique=True, help_text='Número da Cooperativa, máx. 4 dígitos', max_digits=4, decimal_places=0)
    central = models.ForeignKey(
        'central', verbose_name='Central', on_delete=models.CASCADE)
    usuario = models.CharField('Usuario', max_length=150,)
    data = models.DateTimeField(
        'Data e Hora de inclusão', default=timezone.now)

    def __unicode__(self):
        return self.sigla_cooperativa


class pa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_pa = models.CharField('Nome do PA', max_length=50,)
    numpa = models.DecimalField('Número do PA', max_digits=4, decimal_places=0)
    cooperativa = models.ForeignKey(
        'cooperativa', verbose_name='Cooperativa', on_delete=models.CASCADE)
    usuario = models.CharField('Usuario', max_length=150,)
    data = models.DateTimeField(
        'Data e Hora de inclusão', default=timezone.now)

    def clean(self):
        if pa.objects.filter(numpa=self.numpa, cooperativa=self.cooperativa).exists():
            raise ValidationError(_('PA já existente para essa cooperativa'))

    def __unicode__(self):
        return self.cooperativa.sigla_cooperativa + "/" + self.sigla_pa


PFPJ = (
    (0, 'PF'),
    (1, 'PJ'),
)


class cliente(models.Model):
    id = models.AutoField(primary_key=True)
    pa = models.ForeignKey(
        'pa', verbose_name='Cooperativa/PA', on_delete=models.CASCADE)
    tipodepessoa = models.IntegerField(
        'Tipo de Pessoa', choices=PFPJ, default=0)
    numcpfcpnj = models.CharField(
        'Número do CPF/CNPJ', max_length=18, validators=[validate_cpfcpnj])
    nome_cliente = models.CharField('Nome', max_length=50,)
    usuario = models.CharField('Usuario', max_length=150,)
    data = models.DateTimeField(
        'Data e Hora de inclusão', default=timezone.now)

    def __unicode__(self):
        return self.nome_cliente


GRUPOPRODUTOS = (
    (0, 'Menor de 4000'),
    (1, 'Mais de 4000'),
)

TIPOPRODUTO = (
    (0, 'Empréstimo'),
    (2, 'Financiamento'),
    (3, 'Pré aprovado'),
    (4, 'Credito Rural'),
    (5, 'Cheque Especial'),
    (6, 'Cartão de credito'),
    (7, 'Cartão de Debito'),
    (8, 'RDC'),
    (9, 'Poupança'),
    (10, 'Consórcio'),
    (11, 'Sicoob-Previ'),
    (12, 'Sipag'),
    (13, 'Demais seguros'),
    (14, 'Seguro de Vida'),
    (15, 'Débito Automático'),
)


class transacao(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        'Cliente', verbose_name='Cliente', on_delete=models.CASCADE)
    produto = models.IntegerField('Produto', choices=TIPOPRODUTO,)
    grupo = models.IntegerField('Grupo', choices=GRUPOPRODUTOS,)
    usuario = models.CharField('Usuario', max_length=150,)
    data = models.DateTimeField(
        'Data e Hora de inclusão', default=timezone.now)
    vencimento = models.DateField('Vencimento', default=timezone.now(
    ) + timedelta(days=30), validators=[validate_vencimento])

    def clean(self):
        if transacao.objects.filter(Q(cliente=self.cliente) & Q(produto=self.produto) & ~Q(id=self.id)).exists():
            raise ValidationError(_('Produto já existe para esse cliente'))

def update_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('csv/', filename)

class sisbrcsv(models.Model):
    id = models.AutoField(primary_key=True)
    datareferencia = models.DateField('Data de referência',default=timezone.now().date().replace(day=1),)
    sisbrcsvfile = models.FileField('Arquivo csv',upload_to=update_filename)

    def __unicode__(self):
        return str(self.datareferencia)

    def save(self, *args, **kwargs):
        super(sisbrcsv, self).save(*args, **kwargs)
        sisbrtipodeproduto = {
        0: 'TEM_EMPRESTIMO',
        2: 'TEM_FINANCIAMENTO',
        3: 'TEM_PREAPROVADO',
        4: 'TEM_CREDITORURAL',
        5: 'TEM_CHEQUEESPECIAL',
        6: 'TEM_CARTAOCREDITO',
        7: 'TEM_CARTAODEBITO',
        8: 'TEM_RDC',
        9: 'TEM_POUPANCA',
        10: 'TEM_CONSORCIO',
        11: 'TEM_SICOOBPREVI',
        12: 'TEM_SIPAG',
        13: 'TEM_DEMAISSEGUROS',
        14: 'TEM_SEGUROVIDA',
        15: 'TEM_DEBITOAUTOMATICO',
        }
        csvfile = settings.MEDIA_ROOT + "/" + self.sisbrcsvfile.name
        csvfileopen = csv.DictReader(open(csvfile), delimiter=str(u','), dialect=csv.excel)
        for line in csvfileopen:
           if line['NUMCPFCNPJ'] != '':
                if len(line['NUMCPFCNPJ']) == 11:
                    numcpfcpnj = "%s.%s.%s-%s" % ( line['NUMCPFCNPJ'][0:3], line['NUMCPFCNPJ'][3:6], line['NUMCPFCNPJ'][6:9], line['NUMCPFCNPJ'][9:11])
                for key, value in sisbrtipodeproduto.items():
                    if line[value] == '1':
                        produto = key
                        if transacao.objects.filter(Q(cliente__numcpfcpnj=numcpfcpnj) & Q(produto=key)).exists():
                            status = True
                        else:
                            status = False  
                        sisbrprocessainst = sisbrprocessa(sisbrcsv=self,numcpfcpnj=numcpfcpnj,produto=produto,status=status)
                        sisbrprocessainst.save()

class sisbrprocessa(models.Model):
    id = models.AutoField(primary_key=True)
    sisbrcsv = models.ForeignKey(
        'sisbrcsv', verbose_name='Data de referência', on_delete=models.CASCADE)
    numcpfcpnj = models.CharField(
        'Número do CPF/CNPJ', max_length=18,)
    produto = models.IntegerField('Produto',)
    status = models.BooleanField('Status',)
