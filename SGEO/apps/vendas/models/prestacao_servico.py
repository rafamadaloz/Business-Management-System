# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

TIPOS_DESCONTO_ESCOLHAS = (
    (u'0', u'Valor'),
    (u'1', u'Percentual'),
)


class ItensPrestacaoServico(models.Model):
    servico = models.ForeignKey('cadastro.Servico', related_name="servico",
                                on_delete=models.CASCADE, null=True, blank=True)
    prestacao_servico_id = models.ForeignKey(
        'vendas.PrestacaoServico', related_name="itens_venda", on_delete=models.CASCADE)


class PrestacaoServico(models.Model):
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="venda_cliente", on_delete=models.CASCADE)
    vendedor = models.ForeignKey(
        'cadastro.Vendedor', related_name="venda_vendedor", on_delete=models.CASCADE, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    tipo_desconto = models.CharField(
        max_length=1, choices=TIPOS_DESCONTO_ESCOLHAS, default='0')
    desconto = models.DecimalField(max_digits=15, decimal_places=4, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    despesas = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    seguro = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    impostos = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    cond_pagamento = models.ForeignKey(
        'vendas.CondicaoPagamento', related_name="venda_pagamento", on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.CharField(max_length=1055, null=True, blank=True)
