from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse


from SGEO.apps.financeiro.models import Entrada
from SGEO.apps.integracao_financeira.forms import PagSeguroForm, PeriodoIntegracaoForm
from SGEO.apps.integracao_financeira.models import PagSeguro, PeriodoIntegracao
from SGEO.apps.base.custom_views import CustomTemplateView, CustomCreateView
from datetime import datetime
from datetime import timedelta


class PagSeguroView(CustomCreateView):
    template_name = 'integracao_financeira/pagseguro.html'
    success_url = reverse_lazy('integracao_financeira:pagseguroview')
    success_message = "<b>Integração %(id)s </b>adicionada com sucesso."
    permission_codename = 'acessar_ps'
    form_class = PeriodoIntegracaoForm

    def get_initial(self):
        ultima_atualizacao = PeriodoIntegracao.objects.filter(plataforma='PS').last().data_fim
        if ultima_atualizacao:
            return {'data_inicio': ultima_atualizacao, 'data_fim': datetime.now()}

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(PagSeguroView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = form.save()
            self.object.plataforma = 'PS'
            self.object.save()
            return redirect(self.success_url)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ultima_atualizacao = PeriodoIntegracao.objects.filter(plataforma='PS').last().data_fim
        context = super(PagSeguroView, self).get_context_data(**kwargs)
        entradas = Entrada.objects.all()
        context['title_complete'] = 'INTEGRAÇÃO PAGSEGURO'
        context['entradas'] = entradas

        if ultima_atualizacao:
            context['ultima_atualizacao'] = ultima_atualizacao

        return context


class CredenciaisPagSeguroView(CustomTemplateView):
    template_name = 'base/popup_form.html'
    form_class = PagSeguroForm
    model = PagSeguro
    success_url = reverse_lazy('integracao_financeira:pagseguroview')
    success_message = "<b>Oportunidade %(id)s </b>adicionada com sucesso."
    permission_codename = 'integracao_pagseguro'

    def get_context_data(self, **kwargs):
        context = super(CredenciaisPagSeguroView,
                        self).get_context_data(**kwargs)
        context['titulo'] = 'INTEGRAÇÃO PAGSEGURO'
        return context

    def get_object(self):
        try:
            pagseguro = PagSeguro.objects.all()[:1].get()
        except PagSeguro.DoesNotExist:
            pagseguro = PagSeguro.objects.create()

        return pagseguro

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PagSeguroForm(instance=self.object)

        return self.render_to_response(
            self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PagSeguroForm(
            request.POST, request.FILES, instance=self.object)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, object=self.object, ))

def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
