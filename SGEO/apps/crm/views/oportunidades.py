# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView

from SGEO.apps.vendas.forms import OrcamentoVendaForm, PedidoVendaForm, ItensVendaFormSet, PagamentoFormSet
from SGEO.apps.crm.forms import OportunidadeForm
from SGEO.apps.vendas.models import OrcamentoVenda, PedidoVenda, ItensVenda, Pagamento
from SGEO.apps.cadastro.models import MinhaEmpresa
from SGEO.apps.login.models import Usuario
from SGEO.configs.settings import MEDIA_ROOT

from geraldo.generators import PDFGenerator
from datetime import datetime
import io

from .report_vendas import VendaReport

from .forms import OportunidadeForm

class AdicionarOportunidadeView(CustomCreateView):

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, id=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super(AdicionarOportunidadeView, self).get_context_data(**kwargs)
        return self.view_context(context)

    def get(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)
        form.initial['vendedor'] = request.user.first_name or request.user
        form.initial['data_emissao'] = datetime.today().strftime('%d/%m/%Y')

        oportunidade_form = OportunidadeForm(prefix='oportunidade_form')

        return self.render_to_response(self.get_context_data(
                                            form=form,
                                            oportunidade_form=oportunidade_form))

    def post(self, request, form_class, *args, **kwargs):
        self.object = None

        form = self.get_form(form_class)

        oportunidade_form = OportunidadeForm(request.POST, prefix='oportunidade_form')

        if form.is_valid() and oportunidade_form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()

            return self.form_valid(form)

        return self.form_invalid(form=form,
                                 oportunidade_form=oportunidade_form,
                                 )

