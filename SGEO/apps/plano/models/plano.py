# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

RECORRENCIA_OPCOES = [
    ('0', 'Mensal'),
    ('1', 'Anual')
]

STATUS_PAGAMENTO = [
    ('1', 'Aguardando pagamento'),
    ('2', 'Em análise'),
    ('3', 'Paga'),
    ('4', 'Disponível'),
    ('5', 'Em disputa'),
    ('6', 'Devolvida'),
    ('7', 'Cancelada')
]


class TipoPlano(models.Model):
    nome = models.CharField(max_length=32)
    codigo = models.CharField(max_length=15)
    valor_mensal = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])
    valor_anual = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])

    def __unicode__(self):
        s = u'%s' % self.nome
        return s

    def __str__(self):
        s = u'%s' % self.nome
        return s


class NotasAdicionais(models.Model):
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])

    def __unicode__(self):
        s = u'%s' % str(self.quantidade)
        return s

    def __str__(self):
        s = u'%s' % str(self.quantidade)
        return s


class BoletosAdicionais(models.Model):
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])

    def __unicode__(self):
        s = u'%s' % str(self.quantidade)
        return s

    def __str__(self):
        s = u'%s' % str(self.quantidade)
        return s


class UsuariosAdicionais(models.Model):
    quantidade = models.IntegerField(default=0)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])

    def __unicode__(self):
        s = u'%s' % str(self.quantidade)
        return s

    def __str__(self):
        s = u'%s' % str(self.quantidade)
        return s


class Plano(models.Model):
    data_inicio = models.DateField()
    tipo_plano = models.ForeignKey(TipoPlano, related_name='tipo_plano', on_delete=models.CASCADE)
    tipo_pagamento = models.CharField(max_length=1, choices=RECORRENCIA_OPCOES, default=0)
    usuarios_adicionais = models.ForeignKey(UsuariosAdicionais, related_name='usuarios_adicionais', on_delete=models.CASCADE, null=True, blank=True)
    notas_adicionais = models.ForeignKey(NotasAdicionais, related_name='notas_adicionais',
                                            on_delete=models.CASCADE, null=True, blank=True)
    boletos_adicionais = models.ForeignKey(BoletosAdicionais, related_name='boletos_adicionais',
                                            on_delete=models.CASCADE, null=True, blank=True)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])
    codigo_parceiro = models.CharField(null=True, blank=True, max_length=20)
    cupom_desconto = models.CharField(null=True, blank=True, max_length=20)
    cupons_utilizados = models.CharField(null=True, blank=True, max_length=20)
    status_ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Plano"
        permissions = (
            ("view_plano", "Can view plano"),
        )


class Pagamento(models.Model):
    data_criacao = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_PAGAMENTO, default=1)
    codigo = models.CharField(null=True, blank=True, max_length=100)
    valor = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])

