# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'crm2'
urlpatterns = [

    url(r'oportunidade/navegacao/$',
        views.NavegacaoView.as_view(), name='navegacaoview'),

    url(r'oportunidade/funil/$',
        views.FunilView.as_view(), name='funilview'),

    # Pedidos de venda
    #/vendas/pedidovenda/adicionar/
    url(r'oportunidade/adicionar/$',
        views.AdicionarOportunidadeView.as_view(), name='addoportunidadeview'),
    #/vendas/pedidovenda/listapedidovenda
    url(r'oportunidade/lista/$',
        views.OportunidadeListView.as_view(), name='listaoportunidadeview'),
    #/vendas/pedidovenda/editar/
    url(r'oportunidade/editar/(?P<pk>[0-9]+)/$',
        views.EditarOportunidadeView.as_view(), name='editaroportunidadeview'),

    url(r'oportunidade/edit/(?P<pk>[0-9]+)/$',
            views.EditarOportunidadePopupView.as_view(), name='editaroportunidadepopupview'),


    url(r'etiquetas/adicionar/$',
        views.AdicionarEtiquetaView.as_view(), name='addetiquetaview'),

    url(r'etiquetas/lista/$',
        views.EtiquetaView.as_view(), name='etiquetasview'),
    #/vendas/pedidovenda/editar/
    url(r'etiquetas/editar/(?P<pk>[0-9]+)/$',
        views.EditarEtiquetaView.as_view(), name='editaretiquetaview'),


    # Request ajax views
    url(r'infocondpagamento/$', views.InfoCondicaoPagamento.as_view(),
        name='infocondpagamento'),
    url(r'infovenda/$', views.InfoVenda.as_view(), name='infovenda'),


    # Gerar pedido a partir de um orçamento
    url(r'gerarpedidovenda/(?P<pk>[0-9]+)/$',
        views.GerarPedidoVendaView.as_view(), name='gerarpedidovenda'),

    # Cancelar Pedido de venda
    url(r'cancelarpedidovenda/(?P<pk>[0-9]+)/$',
        views.CancelarPedidoVendaView.as_view(), name='cancelarpedidovenda'),
]
