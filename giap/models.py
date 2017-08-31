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

 GRUPOPRODUTOS = (
    (0,'Menor de 4000'),
    (1,'Mais de 4000'),
    )

class produto(models.Model)
    tem_emprestimo = models.BooleanField('Empréstimo')
    tem_financiamento = models.BooleanField('Financiamento')
    tem_preaprovado = models.BooleanField('Pré aprovado')
    tem_creditorural = models.BooleanField('Credito Rural')
    tem_chequeespecial = models.BooleanField('Cheque Especial')
    tem_cartaocredito = models.BooleanField('Cartão de credito')
    tem_cartaodebito = models.BooleanField('Cartão de Debito')
    tem_rdc = models.BooleanField('RDC')
    tem_poupanca = models.BooleanField('Poupança')
    tem_consorcio = models.BooleanField('Consórcio')
    tem_sicoobprevi = models.BooleanField('Sicoob-Previ')
    tem_sipag = models.BooleanField('Sipag')
    tem_demaisseguros = models.BooleanField('Demais seguros')
    tem_segurovida = models.BooleanField('Seguro vida')
    tem_debitoautomatico = models.BooleanField('Débito Automático')
    qtde_produto = models.IntegerField('Quantidade de produtos')
    grupo = models.IntegerField('Grupos',choices=GRUPOPRODUTOS,)

