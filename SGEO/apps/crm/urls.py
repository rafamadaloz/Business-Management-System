# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'crm'

urlpatterns = [
    #/crm/oportunidade/adicionar/
    url(r'oportunidade/adicionar/$',
        views.AdicionarOportunidadeView.as_view(), name='addoportunidadeview'),
    #/crm/oportunidade/listaoportunidades
    url(r'oportunidade/listaclientes/$',
        views.OportunidadesListView.as_view(), name='oportunidadeview'),
    #/crm/oportunidades/editar/
    url(r'oportunidade/editar/(?P<pk>[0-9]+)/$',
        views.EditarOportunidadeView.as_view(), name='editaroportunidadeview'),
]