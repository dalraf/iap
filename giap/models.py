# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cooperativa(models.Model):
    sigla_cooperativa = models.CharField('Nome da Cooperativa',max_length=50,)
    numcooperativa = models.IntegerField('Número da Cooperativa', max_length=6)
    sigla_central = models.CharField('Nome da Central',max_length=50,)
    numcentral = models.IntegerField('Numero da Central', max_length=6)

    def __unicode__(self):
        return self.sigla_cooperativa
    
class pa(models.Model):
    numpa = models.IntegerField('Número do PA', max_length=3)
    cooperativa = models.ForeignKey('cooperativa', verbose_name = 'Cooperativa', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.cooperativa + "-" + self.numpa

 PFPJ = (
    (0,'PF'),
    (1,'PJ'),
    )

class cliente(models.Model)
    pa = models.ForeignKey('pa', verbose_name = 'Cooperativa-PA', on_delete=models.CASCADE)
    tipodepessoa = models.IntegerField('Tipo de Pessoa',choices=PFPJ,)
    numcpfcpnj = models.IntegerField('Número do CPF/CNPJ',max_length=10,)
    nome_cliente = models.CharField('Nome da Cooperativa',max_length=50,)

class usuario(models,Model)
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

class transacao(models.Model)
    usuario = models.ForeignKey('usuario', verbose_name = 'Usuário', on_delete=models.CASCADE)
    cliente = models.ForeignKey('cliente', verbose_name = 'Cliente', on_delete=models.CASCADE)
    qtde_produto = models.IntegerField('Quantidade de produtos')
    produto = models.IntegerField('Grupos',choices=TIPOPRODUTO,)
    grupo = models.IntegerField('Grupos',choices=GRUPOPRODUTOS,)
    data = models.datetime('Data e Hora')

