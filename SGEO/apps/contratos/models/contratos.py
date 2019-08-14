# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

SITUACAO_ESCOLHAS = (
    (u'0', u'Ativo'),
    (u'1', u'Inativo'),
)

TIPO_DURACAO_ESCOLHAS = (
    (u'0', u'Dias'),
    (u'1', u'Semanas'),
    (u'2', u'Meses'),
    (u'3', u'Anos'),
)

INTERVALO_ESCOLHAS = (
    (u'0', u'Dias'),
    (u'1', u'Meses'),
    (u'2', u'Outro Período'),
)

PERIODO_ESCOLHAS = (
    (u'0', u'07/14 dias'),
    (u'1', u'14/28 dias'),
    (u'2', u'15/30 dias'),
    (u'3', u'21/28 dias'),
    (u'4', u'21/42 dias'),
    (u'5', u'28/42 dias'),
    (u'6', u'28/56 dias'),
    (u'7', u'28/35 dias'),
    (u'8', u'30/60 dias'),
    (u'9', u'30/40/50 dias'),
    (u'10', u'35/42 dias'),
    (u'11', u'35/70 dias'),
    (u'12', u'42/84 dias'),
    (u'13', u'45/90 dias'),
    (u'14', u'56/102 dias'),
    (u'15', u'90/180 dias'),
    (u'16', u'Outros'),
)


class Contrato(models.Model):
    empresa = models.ForeignKey(
        'cadastro.Empresa', related_name="contrato_empresa", on_delete=models.CASCADE,
            null=True, blank=True)
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="contrato_cliente", on_delete=models.CASCADE)
    vendedor = models.ForeignKey(
        'cadastro.Vendedor', related_name="contrato_vendedor", on_delete=models.CASCADE, null=True, blank=True)
    tipo_contrato = models.ForeignKey(
        'contratos.TipoContrato', related_name="contrato_tipo", on_delete=models.CASCADE, null=True, blank=True)
    condicao_pagamento = models.ForeignKey(
        'vendas.CondicaoPagamento', related_name="contrato_pagamento", on_delete=models.SET_NULL, null=True)
    centro_custos = models.CharField(max_length=255, null=True, blank=True)
    situacao = models.CharField(max_length=1, choices=SITUACAO_ESCOLHAS, default='0')
    dia_vencimento = models.PositiveIntegerField()
    duracao_contrato = models.PositiveIntegerField()
    tipo_duracao_contrato = models.CharField(max_length=1, choices=TIPO_DURACAO_ESCOLHAS, default=0)
    ultimo_reajuste = models.DateField(null=True, blank=True)
    proximo_reajuste = models.DateField(null=True, blank=True)
    data_termino = models.DateField()
    dias_carencia = models.PositiveIntegerField()
    valor_periodo = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    numero_parcelas = models.PositiveIntegerField()
    intervalo = models.CharField(max_length=1, choices=INTERVALO_ESCOLHAS, default=0)
    periodo = models.CharField(max_length=2, choices=PERIODO_ESCOLHAS, default=0)
    intervalo_dias = models.PositiveIntegerField()
    valor_entrada = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    comissao_vendedor = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_comissao_vendedor_periodo = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    valor_comissao_vendedor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    def __unicode__(self):
        s = u'Orçamento de venda nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Orçamento de venda nº %s' % (self.id)
        return s

    class Meta:
        verbose_name = "Contrato"
        permissions = (
            ("view_contrato", "Can view contrato"),
        )


class TipoContrato(models.Model):
    nome = models.CharField(max_length=255)
    template = models.CharField(max_length=255, null=True, blank=True)






