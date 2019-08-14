# -*- coding: utf-8 -*-

from django.conf.urls import url
from django_pdfkit import PDFView
from . import views

app_name = 'relatorios'
urlpatterns = [
    # Nota fiscal saida
    # /fiscal/notafiscal/saida/adicionar/
    url(r'clientes/$',
        views.RelatorioClientesView.as_view(), name='relatorio_clientes_view'),
    url(r'lancamentos/saidas$',
        views.RelatorioSaidaView.as_view(), name='relatorio_saidas_view'),
    url(r'lancamentos/entradas$',
        views.RelatorioEntradaView.as_view(), name='relatorio_entradas_view'),
    url(r'produtos/$',
        views.RelatorioProdutosView.as_view(), name='relatorio_produtos_view'),
    url(r'vendas/$',
        views.RelatorioVendasView.as_view(), name='relatorio_vendas_view'),
    url(r'dre/$',
        views.DREView.as_view(), name='relatorio_dre_view'),

]