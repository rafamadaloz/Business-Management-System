from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import F

from SGEO.apps.crm2.models import Oportunidade


class FunilView(TemplateView):
    template_name = 'crm2/funil/funil.html'
    permission_codename = 'acesso_funil'

    def get_context_data(self, **kwargs):
        context = super(FunilView, self).get_context_data(**kwargs)
        oportunidades = Oportunidade.objects.all()

        context['oportunidades'] = oportunidades

        return context


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
