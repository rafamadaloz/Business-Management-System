# -*- coding: utf-8 -*-

from django.urls import reverse_lazy

from SGEO.apps.cadastro.forms import VendedorForm
from SGEO.apps.cadastro.models import Vendedor

from .base import AdicionarPessoaView, PessoasListView, EditarPessoaView


class AdicionarVendedorView(AdicionarPessoaView):
    template_name = "cadastro/pessoa_add.html"
    success_url = reverse_lazy('cadastro:listavendedorview')
    success_message = "Vendedor <b>%(nome_razao_social)s </b>adicionado com sucesso."
    permission_codename = 'add_vendedor'

    def get_context_data(self, **kwargs):
        context = super(AdicionarVendedorView, self).get_context_data(**kwargs)
        context['title_complete'] = 'CADASTRAR VENDEDOR'
        context['return_url'] = reverse_lazy('cadastro:listavendedorview')
        context['tipo_pessoa'] = 'vendedor'
        return context

    def get(self, request, *args, **kwargs):
        form = VendedorForm(prefix='vendedor_form')
        return super(AdicionarVendedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['vendedor_form-comissao_vendedor'] = req_post['vendedor_form-comissao_vendedor'].replace(
            '.', '')
        request.POST = req_post
        form = VendedorForm(request.POST, request.FILES,
                           prefix='vendedor_form', request=request)
        return super(AdicionarVendedorView, self).post(request, form, *args, **kwargs)


class VendedorListView(PessoasListView):
    template_name = 'cadastro/pessoa_list.html'
    model = Vendedor
    context_object_name = 'all_vendedores'
    success_url = reverse_lazy('cadastro:listavendedorview')
    permission_codename = 'view_vendedor'

    def get_context_data(self, **kwargs):
        context = super(VendedorListView, self).get_context_data(**kwargs)
        context['title_complete'] = 'VENDEDORES CADASTRADOS'
        context['add_url'] = reverse_lazy('cadastro:addvendedorview')
        context['tipo_pessoa'] = 'vendedor'
        return context


class EditarVendedorView(EditarPessoaView):
    form_class = VendedorForm
    model = Vendedor
    template_name = "cadastro/pessoa_edit.html"
    success_url = reverse_lazy('cadastro:listavendedorview')
    success_message = "Vendedor <b>%(nome_razao_social)s </b>editado com sucesso."
    permission_codename = 'change_vendedor'

    def get_context_data(self, **kwargs):
        context = super(EditarVendedorView, self).get_context_data(**kwargs)
        context['return_url'] = reverse_lazy('cadastro:listavendedorview')
        context['tipo_pessoa'] = 'vendedor'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form_class.prefix = "vendedor_form"
        form = self.get_form(form_class)

        return super(EditarVendedorView, self).get(request, form, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        req_post['vendedor_form-comissao_vendedor'] = req_post['vendedor_form-comissao_vendedor'].replace(
            '.', '')
        request.POST = req_post
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES,
                          prefix='vendedor_form', instance=self.object, request=request)
        return super(EditarVendedorView, self).post(request, form, *args, **kwargs)

