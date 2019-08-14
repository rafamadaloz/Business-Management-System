# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'contratos'
urlpatterns = [

    url(r'adicionar/$',
        views.AdicionarContratoView.as_view(), name='addcontratoview'),
    url(r'lista/$',
        views.ContratosListView.as_view(), name='listacontratosview'),

    url(r'tipo/adicionar/$',
        views.AdicionarTipoContratoView.as_view(template_name='contrato/tipo_contrato/novo_tipo_contrato.html'), name='addtipocontratoview'),
    url(r'tipo/lista/$',
        views.TipoContratoListView.as_view(template_name='contrato/tipo_contrato/lista_tipos_contrato.html'), name='listatiposcontratosview'),
]
