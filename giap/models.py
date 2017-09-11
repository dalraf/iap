# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils import timezone

# Create your models here.

class central(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_central = models.CharField('Nome',unique=True,help_text='Nome da Central',max_length=50,)
    numcentral = models.DecimalField('Número',unique=True,help_text='Número da Central, máx. 4 dígitos', max_digits=4, decimal_places=0, )
    usuario = models.CharField('Nome',max_length=150,)
    data = models.DateTimeField('Data e Hora',default=timezone.now)

    def __unicode__(self):
        return self.sigla_central


class cooperativa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_cooperativa = models.CharField('Nome',unique=True,help_text='Nome da Cooperativa',max_length=50,)
    numcooperativa = models.DecimalField('Número',unique=True,help_text='Número da Cooperativa, máx. 4 dígitos', max_digits=4, decimal_places=0)
    central = models.ForeignKey('central', verbose_name = 'Central', on_delete=models.CASCADE)
    usuario = models.CharField('Nome',max_length=150,)
    data = models.DateTimeField('Data e Hora',default=timezone.now)

    def __unicode__(self):
        return self.sigla_cooperativa
    
class pa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_pa = models.CharField('Nome do PA',unique=True,max_length=50,)
    numpa = models.DecimalField('Número do PA',unique=True,max_digits=4, decimal_places=0 )
    cooperativa = models.ForeignKey('cooperativa', verbose_name = 'Cooperativa', on_delete=models.CASCADE)
    usuario = models.CharField('Nome',max_length=150,)
    data = models.DateTimeField('Data e Hora',default=timezone.now)

    def __unicode__(self):
        return self.cooperativa.sigla_cooperativa + "/" + self.sigla_pa 


PFPJ = (
    (0,'PF'),
    (1,'PJ'),
    )

class cliente(models.Model):
    id = models.AutoField(primary_key=True)
    pa = models.ForeignKey('pa', verbose_name = 'Cooperativa/PA', on_delete=models.CASCADE)
    tipodepessoa = models.IntegerField('Tipo de Pessoa',choices=PFPJ,)
    numcpfcpnj = models.DecimalField('Número do CPF/CNPJ',max_digits=10, decimal_places=0)
    nome_cliente = models.CharField('Nome',max_length=50,)
    usuario = models.CharField('Nome',max_length=150,)
    data = models.DateTimeField('Data e Hora',default=timezone.now)

    def __unicode__(self):
        return self.nome_cliente


GRUPOPRODUTOS = (
        (0,'Menor de 4000'),
        (1,'Mais de 4000'),
        )

TIPOPRODUTO = (
    (0,'Empréstimo'), 
    (2,'Financiamento'), 
    (3,'Pré aprovado'), 
    (4,'Credito Rural'), 
    (5,'Cheque Especial'),
    (6,'Cartão de credito'), 
    (7,'Cartão de Debito'), 
    (8,'RDC'), 
    (9,'Poupança'), 
    (10,'Consórcio'), 
    (11,'Sicoob-Previ'), 
    (12,'Sipag'), 
    (13,'Demais seguros'), 
    (14,'Débito Automático'), 
    (15,'Empréstimo'), 
    )

class transacao(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('Cliente', verbose_name = 'Cliente', on_delete=models.CASCADE)
    produto = models.IntegerField('Produto',choices=TIPOPRODUTO,)
    grupo = models.IntegerField('Grupo',choices=GRUPOPRODUTOS,)
    usuario = models.CharField('Usuario',max_length=150,)
    data = models.DateTimeField('Data e Hora',default=timezone.now)

