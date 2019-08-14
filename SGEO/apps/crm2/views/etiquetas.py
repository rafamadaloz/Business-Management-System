# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from SGEO.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from SGEO.apps.crm2.models import Etiqueta
from SGEO.apps.crm2.forms import EtiquetaForm


class AdicionarEtiquetaView(CustomCreateView):
    template_name = "base/popup_form.html"
    form_class = EtiquetaForm
    model = Etiqueta
    success_url = reverse_lazy('crm2:addetiquetaview')
    permission_codename = 'add_etiqueta'

    def get_context_data(self, **kwargs):
        context = super(AdicionarEtiquetaView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Adicionar Etiqueta'
        return context


class EditarEtiquetaView(CustomUpdateView):
    template_name = "base/popup_form.html"
    form_class = EtiquetaForm
    model = Etiqueta
    success_url = reverse_lazy('crm2:etiquetasview')
    permission_codename = 'change_etiqueta'

    def get_context_data(self, **kwargs):
        context = super(EditarEtiquetaView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'Editar Etiqueta: {0}'.format(str(self.object))
        return context


class EtiquetaView(CustomListView):
    model = Etiqueta
    template_name = 'crm2/navegacao/lista_etiquetas.html'
    context_object_name = 'all_etiquetas'
    success_url = reverse_lazy('crm2:etiquetasview')
    permission_codename = 'view_etiqueta'
