# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

OPCOES_CATEGORIAS = [
    ('0', 'Consumidor Final'),
    ('1', 'Garantia'),
    ('2', 'Remessa'),
    ('3', 'Venda Externa'),
    ('4', 'Venda Loja'),
    ('5', 'Venda de Materiais e Serviços'),
    ('6', 'Venda Mercado Livre'),
    ('7', 'Vendas Site'),
]

class Oportunidade(models.Model):
    empresa = models.ForeignKey(
        'cadastro.Empresa', related_name = "oportunidade_empresa", on_delete=models.CASCADE)
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="oportunidade_cliente", on_delete=models.CASCADE)
    categoria = models.CharField(
        max_length=1, choices=OPCOES_CATEGORIAS)

    class Meta:
        verbose_name = "Oportunidade"
        permissions = (
            ("view_oportunidade", "Can view Oportunidade"),
        )

    def edit_url(self):
        return reverse_lazy('crm:oportunidadeview', kwargs={'pk': self.id})

    def __unicode__(self):
        s = u'Oportunidade nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Oportunidade nº %s' % (self.id)
        return s