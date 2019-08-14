import django_filters
from SGEO.apps.financeiro.models import Entrada
from SGEO.apps.cadastro.models import Cliente
from django.db import models
from django import forms


class EntradaFilter(django_filters.FilterSet):
    class Meta:
        model = Entrada
        fields = ['data_emissao', 'data_vencimento', 'data_pagamento']


class ClienteFilter(django_filters.FilterSet):
    class Meta:
        model = Cliente
        fields = {
            'nome_razao_social': ['icontains'],
        }

