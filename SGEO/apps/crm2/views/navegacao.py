from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import F
from django.urls import reverse_lazy

from SGEO.apps.cadastro.models import StatusVenda
from SGEO.apps.crm2.models import Oportunidade
from SGEO.apps.crm2.forms import OportunidadeForm
from SGEO.apps.base.custom_views import CustomCreateView


class NavegacaoView(CustomCreateView):
    template_name = 'crm2/navegacao/navegacao.html'
    form_class = OportunidadeForm
    success_message = "<b>Oportunidade %(id)s </b>adicionada com sucesso."
    permission_codename = 'acesso_navegacao'
    success_url = reverse_lazy('crm2:navegacaoview')

    def get_context_data(self, **kwargs):
        context = super(NavegacaoView, self).get_context_data(**kwargs)
        status_vendas = StatusVenda.objects.all()
        oportunidades = Oportunidade.objects.all()

        context['status_vendas'] = status_vendas
        context['oportunidades'] = oportunidades

        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(NavegacaoView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(NavegacaoView, self).post(request, form_class, *args, **kwargs)


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
