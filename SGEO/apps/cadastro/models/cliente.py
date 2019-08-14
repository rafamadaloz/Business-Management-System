# -*- coding: utf-8 -*-

from django.db import models

from decimal import Decimal

from .base import Pessoa

INDICADOR_IE_DEST = [
    ('1', 'Contribuinte ICMS'),
    ('2', 'Contribuinte isento de Inscrição'),
    ('9', 'Não Contribuinte'),
]


class Cliente(Pessoa):
    limite_de_credito = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    limite_restante = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    indicador_ie = models.CharField(
        max_length=1, choices=INDICADOR_IE_DEST, default='9')
    id_estrangeiro = models.CharField(max_length=20, null=True, blank=True)
    grupo = models.ForeignKey('cadastro.Grupo', related_name="grupo",
                              on_delete=models.CASCADE, null=True, blank=True)
    comissao_vendedor = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    proxima_visita = models.DateField(null=True, blank=True)
    valor_total_vendas = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'))


    class Meta:
        verbose_name = "Cliente"
        permissions = (
            ("view_cliente", "Can view cliente"),
        )


class Grupo(models.Model):
    grupo_desc = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Grupo"
        permissions = (
            ("view_grupo", "Can view grupo"),
        )

    def __unicode__(self):
        s = u'%s' % (self.grupo_desc)
        return s

    def __str__(self):
        s = u'%s' % (self.grupo_desc)
        return s

