# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class central(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_central = models.CharField('Nome',help_text='Nome da cooperativa',max_length=50,)
    numcentral = models.DecimalField('Número',help_text='Número da cooperativa, máx. 4 dígitos', max_digits=4, decimal_places=0, )

    def __unicode__(self):
        return self.sigla_cooperativa


class cooperativa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_cooperativa = models.CharField('Nome da Cooperativa',max_length=50,)
    numcooperativa = models.DecimalField('Número da Cooperativa',max_digits=4, decimal_places=0)
    central = models.ForeignKey('central', verbose_name = 'Central', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.sigla_cooperativa
    
class pa(models.Model):
    id = models.AutoField(primary_key=True)
    sigla_pa = models.CharField('Nome do PA',max_length=50,)
    numpa = models.DecimalField('Número do PA',max_digits=4, decimal_places=0 )
    cooperativa = models.ForeignKey('cooperativa', verbose_name = 'Cooperativa', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.cooperativa + "-" + self.numpa


PFPJ = (
    (0,'PF'),
    (1,'PJ'),
    )

class cliente(models.Model):
    pa = models.ForeignKey('pa', verbose_name = 'Cooperativa-PA', on_delete=models.CASCADE)
    tipodepessoa = models.IntegerField('Tipo de Pessoa',choices=PFPJ,)
    numcpfcpnj = models.DecimalField('Número do CPF/CNPJ',max_digits=10, decimal_places=0)
    nome_cliente = models.CharField('Nome da Cooperativa',max_length=50,)

class usuario(models.Model):
    nome = models.CharField('Nome da Cooperativa',max_length=50,)   

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
    usuario = models.ForeignKey('usuario', verbose_name = 'Usuário', on_delete=models.CASCADE)
    cliente = models.ForeignKey('cliente', verbose_name = 'Cliente', on_delete=models.CASCADE)
    qtde_produto = models.IntegerField('Quantidade de produtos')
    produto = models.IntegerField('Grupos',choices=TIPOPRODUTO,)
    grupo = models.IntegerField('Grupos',choices=GRUPOPRODUTOS,)
    data = models.DateTimeField('Data e Hora')

