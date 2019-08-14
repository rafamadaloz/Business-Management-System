# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

TIPOS_ESCOLHAS = (
    ('0', 'Prestado'),
    ('1', 'Tomado'),
    ('2', 'Prestado e Tomado')
)


class Servico(models.Model):
    codigo = models.CharField(max_length=15)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=1, choices=TIPOS_ESCOLHAS, default='0')
    categoria = models.ForeignKey(
        'cadastro.Categoria', null=True, blank=True, on_delete=models.PROTECT)
    valor_venda = models.DecimalField(max_digits=16, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_custo = models.DecimalField(max_digits=16, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    inf_adicionais = models.CharField(max_length=255, null=True, blank=True)
    nbs = models.CharField(max_length=15, null=True, blank=True)
    codigo_tributacao_municipal = models.CharField(max_length=15, null=True, blank=True)
    codigo_municipal_servico = models.CharField(max_length=15, null=True, blank=True)
    status_ativo = models.BooleanField(default=True)
