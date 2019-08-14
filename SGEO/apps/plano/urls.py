# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'plano'
urlpatterns = [

    url(r'adicionar/$', views.AdicionarPlanoView.as_view(),
        name='adicionarplanoview'),

    url(r'meu_plano/$', views.MeuPlanoView.as_view(),
            name='meuplanoview'),

]
