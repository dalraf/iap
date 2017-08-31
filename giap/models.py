# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cooperativa(models.Model):
    sigla_cooperativa = models.CharField('Nome da Cooperativa',max_length=50,)
    numcooperativa = models.IntegerField('Número da Cooperativa', max_length=6)
    sigla_central = models.CharField('Nome da Central',max_length=50,)
    numcentral = models.IntegerField('Numero da Central', max_length=6)
    

