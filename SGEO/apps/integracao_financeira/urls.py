# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'integracao_financeira'
urlpatterns = [
    url(r'hotmart/dashboard/$',
        views.HotmartView.as_view(), name='hotmartview'),
    url(r'eduzz/dashboard/$',
        views.EduzzView.as_view(), name='eduzzview'),
    url(r'mercadopago/dashboard/$',
        views.MercadoPagoView.as_view(), name='mercadopagoview'),
    url(r'pagseguro/dashboard/$',
        views.PagSeguroView.as_view(), name='pagseguroview'),

    url(r'pagseguro/credenciais/$',
            views.CredenciaisPagSeguroView.as_view(), name='credenciaisPSview'),

]