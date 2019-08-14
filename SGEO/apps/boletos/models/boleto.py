# -*- coding: utf-8 -*-

from django.db import models

STATUS_OPCOES = [
    ('0', 'Em digitação'),
    ('1', 'Emitido'),
]


class Boleto(models.Model):
    token = models.CharField(max_length=255, null=True, blank=True)
    pedido_de_venda = models.ForeignKey(
        'vendas.PedidoVenda',
        related_name="pedido_boleto",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    pagador = models.ForeignKey(
        'cadastro.Cliente',
        related_name="pagador_boleto",
        on_delete=models.CASCADE
    )
    emissao = models.DateField()
    vencimento = models.DateField()
    documento = models.CharField(max_length=32)
    numero = models.CharField(max_length=32)
    titulo = models.CharField(max_length=32)
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=2, choices=STATUS_OPCOES)

    class Meta:
        verbose_name = "Boleto"
        permissions = (
            ("view_boleto", "Can view boleto"),
        )


