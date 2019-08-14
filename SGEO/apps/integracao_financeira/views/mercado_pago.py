from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import F

from SGEO.apps.financeiro.models import Entrada
from SGEO.apps.integracao_financeira.forms import MercadoPagoForm
from SGEO.apps.base.custom_views import CustomCreateView



class MercadoPagoView(CustomCreateView):
    template_name = 'integracao_financeira/mercado_pago.html'
    form_class = MercadoPagoForm
    success_message = "<b>Oportunidade %(id)s </b>adicionada com sucesso."
    permission_codename = 'acessar_mp'

    def get_context_data(self, **kwargs):
        context = super(MercadoPagoView, self).get_context_data(**kwargs)
        entradas = Entrada.objects.all()
        context['title_complete'] = 'INTEGRAÇÃO MERCADO PAGO'
        context['entradas'] = entradas

        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(MercadoPagoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(MercadoPagoView, self).post(request, form_class, *args, **kwargs)


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
