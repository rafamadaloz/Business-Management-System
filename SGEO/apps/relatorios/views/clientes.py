# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import FileResponse
from django.db.models.functions import Extract

from SGEO.apps.base.custom_views import CustomView, CustomCreateView, CustomListView, CustomUpdateView
from django.views.generic import View
from django.utils import timezone
from .render import Render
from SGEO.apps.cadastro.models import Cliente, MinhaEmpresa
from SGEO.apps.login.models import Usuario
from SGEO.apps.relatorios.tables import ClienteTable, Cliente2Table
import pdfkit
from django.template import Context
from django.template.loader import get_template
import os
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime

from SGEO.apps.base.custom_views import CustomView
from django.template.loader import render_to_string
from django.http import HttpResponse
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from SGEO.apps.relatorios.filter import ClienteFilter
from django.urls import reverse_lazy
from django_tables2.views import SingleTableMixin, SingleTableView
import pytz


from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class RelatorioClientesView(SingleTableMixin, ExportMixin, CustomListView):
    template_name = 'relatorios/clientes/geral.html'
    model = Cliente
    table_class = ClienteTable
    context_object_name = 'all_clientes'
    permission_codename = 'acessar_relatorio_clientes'
    success_url = reverse_lazy('relatorios:relatorio_clientes_view')

    def get_context_data(self, **kwargs):
        context = super(RelatorioClientesView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'Relatório de Clientes'
        context['aniversariantes'] = self.model.objects.annotate(
            pessoa_fis_info__nascimento__month=Extract('pessoa_fis_info__nascimento', 'month'),
            pessoa_fis_info__nascimento__day=Extract('pessoa_fis_info__nascimento', 'day')
            ).order_by('pessoa_fis_info__nascimento__month', 'pessoa_fis_info__nascimento__day')\
            .filter(pessoa_fis_info__nascimento__day__gte=datetime.now().day,
                    pessoa_fis_info__nascimento__month__gte=datetime.now().month
                    )[:6]

        context['maiores_vendas'] = self.model.objects.order_by('-valor_total_vendas')[:10]
        context['maiores_vendas'] = reversed(context['maiores_vendas'])

        table = ClienteTable(Cliente.objects.all())
        table.paginate(page=self.request.GET.get('page', 1), per_page=15)

        context['table'] = table
        RequestConfig(self.request).configure(table)

        return context

