# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

STATUS__VENDA_PDV_ESCOLHAS = (
    (u'0', u'Aberto'),
    (u'1', u'Faturado'),
)

class ProdutoPDV(models.Model):

    produto = models.ForeignKey(
        'cadastro.Produto', related_name="produto_pdv", on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    valor_unit = models.DecimalField(max_digits=12, decimal_places=2, validators=[
                                MinValueValidator(Decimal('0.00'))])


class VendaPdv(models.Model):
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="venda_pdv_cliente", on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.CharField(max_length=60, null=True, blank=True)
    data_emissao = models.DateTimeField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    pagamento = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS__VENDA_PDV_ESCOLHAS, default='0')


class ItensVendaPdv(models.Model):
    produto = models.ForeignKey('cadastro.Produto', related_name="venda_pdv_produto",
                                on_delete=models.CASCADE, null=True, blank=True)
    venda_pdv_id = models.ForeignKey(
        VendaPdv, related_name="itens_venda_pdv", on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    valor_unit = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    subtotal = models.DecimalField(max_digits=13, decimal_places=2, validators=[
        MinValueValidator(Decimal('0.00'))], null=True, blank=True)
