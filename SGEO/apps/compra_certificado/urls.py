# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'compra_certificado'

urlpatterns = [
    url(r'formulario/$',
        views.FormularioCompraCertificadoView.as_view(), name='viewformulario'),
    url(r'cadastro/$',
        views.AdicionarSocioAdministrativoView.as_view(), name='addsocioadmview'),
]