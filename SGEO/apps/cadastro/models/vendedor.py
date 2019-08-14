# -*- coding: utf-8 -*-

from django.db import models

from decimal import Decimal

from .base import Pessoa

class Vendedor(Pessoa):
    comissao_vendedor = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    horas_trabalhadas_por_dia = models.DurationField(blank=True, null=True)
    dias_folga_por_semana = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Vendedor"
        permissions = (
            ("view_vendedor", "Can view vendedor"),
        )
