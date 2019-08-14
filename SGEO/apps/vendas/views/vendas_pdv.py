# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView

from SGEO.apps.pdv.models import VendaPdv


class VendasPdvListView(CustomListView):
    template_name = 'vendas/vendas_pdv/lista_vendas_pdv.html'
    model = VendaPdv
    context_object_name = 'all_vendas'
    success_url = reverse_lazy('vendas:listapedidovendaview')
    permission_codename = 'view_vendas_pdv'

    def view_context(self, context):
        context['title_complete'] = 'FRENTE DE CAIXA'
        context['add_url'] = reverse_lazy('vendas:addpedidovendaview')
        return context

    def get_context_data(self, **kwargs):
        context = super(VendasPdvListView, self).get_context_data(**kwargs)
        return self.view_context(context)
