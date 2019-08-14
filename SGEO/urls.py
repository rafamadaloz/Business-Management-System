# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from .configs.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('SGEO.apps.base.urls')),
    url(r'^login/', include('SGEO.apps.login.urls')),
    url(r'^cadastro/', include('SGEO.apps.cadastro.urls')),
    url(r'^fiscal/', include('SGEO.apps.fiscal.urls')),
    url(r'^vendas/', include('SGEO.apps.vendas.urls')),
    url(r'^compras/', include('SGEO.apps.compras.urls')),
    url(r'^financeiro/', include('SGEO.apps.financeiro.urls')),
    url(r'^estoque/', include('SGEO.apps.estoque.urls')),
    url(r'^agenda/', include('SGEO.apps.agenda.urls')),
    url(r'^boletos/', include('SGEO.apps.boletos.urls')),
    url(r'^crm2/', include('SGEO.apps.crm2.urls')),
    url(r'^pdv/', include('SGEO.apps.pdv.urls')),
    url(r'^customer/', include('SGEO.apps.customer.urls')),
    url(r'^relatorios/', include('SGEO.apps.relatorios.urls')),
    url(r'^plano/', include('SGEO.apps.plano.urls')),
    url(r'^compra_certificado/', include('SGEO.apps.compra_certificado.urls')),
    url(r'^contratos/', include('SGEO.apps.contratos.urls')),
    url(r'^integracao_financeira/', include('SGEO.apps.integracao_financeira.urls')),
]

if DEBUG is True:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
