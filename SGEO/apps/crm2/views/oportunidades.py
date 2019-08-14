# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView

from SGEO.apps.vendas.forms import OrcamentoVendaForm, PedidoVendaForm, ItensVendaFormSet, PagamentoFormSet
from SGEO.apps.vendas.models import OrcamentoVenda, PedidoVenda, ItensVenda, Pagamento
from SGEO.apps.crm2.models import Oportunidade
from SGEO.apps.cadastro.models import StatusVenda
from SGEO.apps.login.models import Usuario
from SGEO.configs.settings import MEDIA_ROOT

from SGEO.apps.crm2.forms import OportunidadeForm

from geraldo.generators import PDFGenerator
from datetime import datetime
import io

from .report_vendas import VendaReport

class SalvarOportunidadeView(CustomCreateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(SalvarOportunidadeView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        form.initial['vendedor'] = request.user.first_name or request.user
        form.initial['data_emissao'] = datetime.today().strftime('%d/%m/%Y')

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if (
                    'valor' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form = self.get_form(form_class)

        if (form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form)


class AdicionarOportunidadeView(SalvarOportunidadeView):
    form_class = OportunidadeForm
    template_name = "crm2/oportunidade/oportunidade_add.html"
    success_url = reverse_lazy('crm2:listaoportunidadeview')
    success_message = "<b>Oportunidade %(id)s </b>adicionada com sucesso."
    permission_codename = 'add_oportunidade'

    def view_context(self, context):
        context['title_complete'] = 'ADICIONAR OPORTUNIDADE'
        context['return_url'] = reverse_lazy('crm2:listaoportunidadeview')
        return context

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOportunidadeView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        return super(AdicionarOportunidadeView, self).post(request, form_class, *args, **kwargs)


class OportunidadeView(CustomListView):

    def get_context_data(self, **kwargs):
        context = super(OportunidadeView, self).get_context_data(**kwargs)
        return self.view_context(context)


class OportunidadeListView(OportunidadeView):
    template_name = 'crm2/oportunidade/oportunidade_list.html'
    model = Oportunidade
    context_object_name = 'all_oportunidades'
    success_url = reverse_lazy('crm2:listaoportunidadeview')
    permission_codename = 'view_oportunidade'

    def view_context(self, context):
        context['title_complete'] = 'OPORTUNIDADES'
        context['add_url'] = reverse_lazy('crm2:addoportunidadeview')
        return context

class EditarVendaView(CustomUpdateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(EditarVendaView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):

        form = self.get_form(form_class)

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, form_class, *args, **kwargs):
        self.object = None
        # Tirar . dos campos decimais
        req_post = request.POST.copy()

        for key in req_post:
            if ('probabilidade_fechamento' in key or
                    'valor' in key):
                req_post[key] = req_post[key].replace('.', '')

        request.POST = req_post

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if (form.is_valid()):
            self.object = form.save(commit=False)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form)


class EditarOportunidadeView(CustomUpdateView):
    form_class = OportunidadeForm
    model = Oportunidade
    template_name = "crm2/oportunidade/oportunidade_edit.html"
    success_url = reverse_lazy('crm2:listaoportunidadeview')
    success_message = "<b>Oportunidade %(id)s </b>editada com sucesso."
    permission_codename = 'change_oportunidade'

    def view_context(self, context):
        context['title_complete'] = 'EDITAR OPORTUNIDADE N°' + \
            str(self.object.id)
        context['return_url'] = reverse_lazy('crm2:listaoportunidadeview')
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarOportunidadeView, self).get(request, form_class, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        return super(EditarOportunidadeView, self).post(request, form_class, *args, **kwargs)


class EditarOportunidadePopupView(CustomUpdateView):
    template_name = "crm2/oportunidade/oportunidade_edit_popup.html"
    form_class = OportunidadeForm
    model = Oportunidade
    success_url = reverse_lazy('crm2:navegacaoview')
    permission_codename = 'change_oportunidade'

    def get_context_data(self, **kwargs):
        context = super(EditarOportunidadePopupView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'EDITAR OPORTUNIDADE N°' + \
                                    str(self.object.id)
        return context


class GerarPedidoVendaView(CustomView):
    permission_codename = ['add_oportunidade', 'change_pedidovenda', ]

    def get(self, request, *args, **kwargs):
        orcamento_id = kwargs.get('pk', None)
        orcamento = OrcamentoVenda.objects.get(id=orcamento_id)
        itens_venda = orcamento.itens_venda.all()
        pagamentos = orcamento.parcela_pagamento.all()
        novo_pedido = PedidoVenda()

        for field in orcamento._meta.fields:
            setattr(novo_pedido, field.name, getattr(orcamento, field.name))

        novo_pedido.venda_ptr = None
        novo_pedido.pk = None
        novo_pedido.id = None
        novo_pedido.status = '0'
        orcamento.status = '1'  # Baixado
        orcamento.save()
        novo_pedido.orcamento = orcamento
        novo_pedido.save()

        for item in itens_venda:
            item.pk = None
            item.id = None
            item.save()
            novo_pedido.itens_venda.add(item)

        for pagamento in pagamentos:
            pagamento.pk = None
            pagamento.id = None
            pagamento.save()
            novo_pedido.parcela_pagamento.add(pagamento)

        return redirect(reverse_lazy('vendas:editarpedidovendaview', kwargs={'pk': novo_pedido.id}))


class CancelarPedidoVendaView(CustomView):
    permission_codename = 'change_pedidovenda'

    def get(self, request, *args, **kwargs):
        venda_id = kwargs.get('pk', None)
        instance = PedidoVenda.objects.get(id=venda_id)
        instance.status = '2'
        instance.save()
        return redirect(reverse_lazy('vendas:editarpedidovendaview', kwargs={'pk': instance.id}))



