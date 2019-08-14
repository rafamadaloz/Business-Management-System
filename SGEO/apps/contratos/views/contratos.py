# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView
from SGEO.apps.contratos.forms import ContratoForm, TipoContratoForm
from SGEO.apps.contratos.models import Contrato, TipoContrato


class AdicionarContratoView(CustomCreateView):

    form_class = ContratoForm
    template_name = "contratos/novo_contrato.html"
    success_url = reverse_lazy('contratos:listacontratosview')
    success_message = "<b>Contrato %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_contrato'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR CONTRATO'
        context['return_url'] = reverse_lazy('contratos:listacontratosview')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarContratoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarContratoView, self).post(request, form_class, *args, **kwargs)


class ContratosListView(CustomListView):
    template_name = 'contratos/lista_contratos.html'
    model = Contrato
    context_object_name = 'all_contratos'
    success_url = reverse_lazy('contratos:listacontratosview')
    permission_codename = 'view_contrato'

    def get_context_data(self, **kwargs):
        context = super(ContratosListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'CONTRATOS CADASTRADOS'
        context['add_url'] = reverse_lazy('contratos:addcontratoview')
        return context


class AdicionarTipoContratoView(CustomCreateView):

    form_class = TipoContratoForm
    template_name = "contratos/tipo_contrato/novo_tipo_contrato.html"
    success_url = reverse_lazy('contratos:listatiposcontratosview')
    success_message = "<b>Tipo de Contrato %(id)s </b>adicionado com sucesso."
    permission_codename = 'add_tipo_contrato'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR TIPO DE CONTRATO'
        context['return_url'] = reverse_lazy('contratos:listatiposcontratosview')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarTipoContratoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarTipoContratoView, self).post(request, form_class, *args, **kwargs)


class TipoContratoListView(CustomListView):
    template_name = 'contratos/tipo_contrato/lista_tipos_contrato.html'
    model = TipoContrato
    context_object_name = 'all_tipos_contratos'
    success_url = reverse_lazy('contratos:listatiposcontratosview')
    permission_codename = 'view_tipos_contratos'

    def get_context_data(self, **kwargs):
        context = super(TipoContratoListView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'TIPOS DE CONTRATOS CADASTRADOS'
        context['add_url'] = reverse_lazy('contratos:addtipocontratoview')
        return context
