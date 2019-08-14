# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic.list import ListView


from SGEO.apps.base.custom_views import CustomCreateView, CustomListView, CustomUpdateView
from SGEO.apps.cadastro.forms import ServicoForm
from SGEO.apps.cadastro.models import Servico

class AdicionarServicoView(CustomCreateView):
    form_class = ServicoForm
    template_name = "cadastro/servico/servico_add.html"
    success_url = reverse_lazy('cadastro:listaservicosview')
    success_message = "Serviço <b>%(descricao)s </b>adicionado com sucesso."
    permission_codename = 'add_servico'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(AdicionarServicoView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR SERVIÇO'
        context['return_url'] = reverse_lazy('cadastro:listaservicosview')
        return context

    def get(self, request, *args, **kwargs):
        return super(AdicionarServicoView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if ('valor_venda' in key or
                    'valor_custo' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
            return self.form_valid(form)

        return self.form_invalid(form)

class ServicosListView(CustomListView):
    template_name = 'cadastro/servico/servico_list.html'
    model = Servico
    context_object_name = 'all_servicos'
    success_url = reverse_lazy('cadastro:listaservicosview')
    permission_codename = 'view_servico'

    def get_context_data(self, **kwargs):
        context = super(ServicosListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'SERVIÇOS CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addservicoview')
        return context


class EditarServicoView(CustomUpdateView):
    form_class = ServicoForm
    model = Servico
    template_name = "cadastro/servico/servico_edit.html"
    success_url = reverse_lazy('cadastro:listaservicosview')
    success_message = "Serviço <b>%(descricao)s </b>editado com sucesso."
    permission_codename = 'change_servico'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, descricao=self.object.descricao)

    def get_context_data(self, **kwargs):
        context = super(EditarServicoView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listaservicosview')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if ('valor_venda' in key or
                    'valor_atual' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = form_class(request.POST, instance=self.object)

        if form.is_valid():
            self.object = form.save()
            return self.form_valid(form)

        return self.form_invalid(form)
