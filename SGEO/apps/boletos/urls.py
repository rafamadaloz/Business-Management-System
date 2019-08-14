# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'boletos'
urlpatterns = [

    url(r'configuracao/editar/(?P<pk>[0-9]+)/$', views.EditarConfiguracaoBoletoView.as_view(),
        name='editarconfiguracaoboletoview'),

    url(r'configuracao/adicionar/$', views.AdicionarConfiguracaoBoletoView.as_view(),
        name='adicionarconfiguracaoboletoview'),

    url(r'boletos/adicionar/$', views.AdicionarBoletoAvulsoView.as_view(),
        name='adicionarboletoavulsoview'),

    url(r'boletos/editar/(?P<pk>[0-9]+)/$', views.EditarBoletoAvulsoView.as_view(),
        name='editarboletoavulsoview'),

    url(r'boletos/$', views.BoletosListView.as_view(),
        name='listaboletosview'),

    url(r'boletos/gerarPDF/(?P<pk>[0-9]+)/$', views.GerarPDFBoleto.as_view(),
        name='gerarpdfboletoview'),
]
