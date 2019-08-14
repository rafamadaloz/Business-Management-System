from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import F

from SGEO.apps.financeiro.models import Entrada
from SGEO.apps.integracao_financeira.forms import EduzzForm
from SGEO.apps.base.custom_views import CustomCreateView



class EduzzView(CustomCreateView):
    template_name = 'integracao_financeira/eduzz.html'
    form_class = EduzzForm
    success_message = "<b>Oportunidade %(id)s </b>adicionada com sucesso."
    permission_codename = 'acessar_eduzz'

    def get_context_data(self, **kwargs):
        context = super(EduzzView, self).get_context_data(**kwargs)
        entradas = Entrada.objects.all()
        context['title_complete'] = 'INTEGRAÇÃO EDUZZ'
        context['entradas'] = entradas

        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(EduzzView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(EduzzView, self).post(request, form_class, *args, **kwargs)


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
