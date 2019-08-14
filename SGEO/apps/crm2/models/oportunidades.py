# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import date
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy

from decimal import Decimal

from SGEO.apps.fiscal.models import PIS, COFINS
from SGEO.apps.estoque.models import DEFAULT_LOCAL_ID

import locale
locale.setlocale(locale.LC_ALL, '')

CATEGORIAS = (
    (u'0', u'Consumidor Final'),
    (u'1', u'Garantia'),
    (u'2', u'Remessa'),
    (u'3', u'Venda Externa'),
    (u'4', u'Venda Loja'),
    (u'5', u'Venda de Materiais e Serviços'),
    (u'6', u'Vendas Site')
)

ORIGEM_OPCOES = (
    (u'IE', u'Indicação Externa'),
    (u'II', u'Indicação Interna'),
    (u'BB', u'Boca a Boca'),
    (u'WE', u'Web'),
    (u'PA', u'Parceiro'),
    (u'CA', u'Campanha'),
    (u'LO', u'Loja'),
    (u'PV', u'Ponto de Venda Externo'),
    (u'RA', u'Rádio'),
    (u'JI', u'Jornal Impressp'),
    (u'OU', u'Outro')
)

SITUACAO_OPCOES = (
    (u'0', u'Concluída com sucesso'),
    (u'1', u'Cancelado'),
    (u'2', u'Em andamento')
)


class Oportunidade(models.Model):
    cliente = models.ForeignKey(
        'cadastro.Cliente', related_name="oportunidade_cliente", on_delete=models.CASCADE
    )
    empresa = models.ForeignKey(
        'cadastro.Empresa', related_name="oportunidade_empresa", on_delete=models.CASCADE, null=True, blank=True
    )

    status_venda = models.ForeignKey(
        'cadastro.StatusVenda', related_name="oportunidade_status_venda", on_delete=models.CASCADE,
        null=True, blank=True
    )

    etiquetas = models.ManyToManyField('crm2.Etiqueta', blank=True)

    categoria = models.CharField(
        max_length=1, choices=CATEGORIAS, null=True, blank=True)

    responsavel = models.CharField(max_length=255, null=True, blank=True)

    descricao = models.CharField(max_length=1000, null=True, blank=True)

    data_abertura = models.DateField(null=True, blank=True)

    data_fechamento = models.DateField(null=True, blank=True)

    probabilidade_fechamento = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    valor = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True)

    contato = models.CharField(max_length=255, null=True, blank=True)

    origem = models.CharField(max_length=2, choices=ORIGEM_OPCOES, null=True, blank=True)

    nome_origem = models.CharField(max_length=255, null=True, blank=True)

    situacao = models.CharField(max_length=1, choices=SITUACAO_OPCOES, default=2)

    data_sucesso = models.DateField(null=True, blank=True)

    data_cancelamento = models.DateField(null=True, blank=True)

    motivo_cancelamento = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = "Oportunidade"
        permissions = (
            ("view_oportunidade", "Can view oportunidade"),
            ("acesso_navegacao", "Pode acessar a navegacao"),
            ("acesso_funil", "Pode acessar o funil"),
        )


    def __unicode__(self):
        s = u'Venda nº %s' % (self.id)
        return s

    def __str__(self):
        s = u'Venda nº %s' % (self.id)
        return s





