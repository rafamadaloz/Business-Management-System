# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
from SGEO.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from SGEO.apps.compra_certificado.forms import CadastroCompraCertificadoA1Form

class FormularioCompraCertificadoView(TemplateView):
    template_name = 'compra_certificado/formulario.html'
    def get_context_data(self, **kwargs):
        context = super(FormularioCompraCertificadoView, self).get_context_data(**kwargs)

        return context


class AdicionarSocioAdministrativoView(CustomCreateView):
    form_class = CadastroCompraCertificadoA1Form
    template_name = "compra_certificado/cadastro.html"
    permission_codename = 'add_socio_adm'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarSocioAdministrativoView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'DADOS CADASTRAIS'
        return context

def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
