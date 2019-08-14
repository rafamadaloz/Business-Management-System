from SGEO.apps.financeiro.models import Entrada, MovimentoCaixa
from SGEO.apps.relatorios.tables import EntradasTable
from SGEO.apps.base.custom_views import CustomListView
from django_tables2.export.views import ExportMixin
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView


class RelatorioEntradaView(ExportMixin, CustomListView):
    template_name = 'relatorios/lancamentos/geral.html'
    model = Entrada
    table_class = EntradasTable
    context_object_name = 'all_lancamentos'
    permission_codename = 'acessar_relatorio_entradas'

    def get_context_data(self, **kwargs):
        context = super(RelatorioEntradaView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'Relatório de Lançamentos (Entradas)'
        context['tipo_lancamento'] = 'entrada'

        context['all_movimentos'] = MovimentoCaixa.objects.order_by('data_movimento')

        table = self.table_class(self.model.objects.all())
        table.paginate(page=self.request.GET.get('page', 1), per_page=15)
        table.exclude = ('lancamento_ptr')

        context['table'] = table
        RequestConfig(self.request).configure(table) #ordena

        export_format = self.request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, table)
            return exporter.response('File_Name.{}'.format(export_format))

        return context


class RelatorioSaidaView(ExportMixin, CustomListView):
    template_name = 'relatorios/lancamentos/geral.html'
    model = Entrada
    table_class = EntradasTable
    context_object_name = 'all_lancamentos'
    permission_codename = 'acessar_relatorio_saidas'

    def get_context_data(self, **kwargs):
        context = super(RelatorioSaidaView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'Relatório de Lançamentos (Saídas)'
        context['tipo_lancamento'] = 'saida'
        context['all_movimentos'] = MovimentoCaixa.objects.order_by('data_movimento')

        table = self.table_class(self.model.objects.all())
        table.paginate(page=self.request.GET.get('page', 1), per_page=15)
        table.exclude = ('lancamento_ptr')

        context['table'] = table
        RequestConfig(self.request).configure(table) #ordena

        export_format = self.request.GET.get('_export', None)
        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, table)
            return exporter.response('File_Name.{}'.format(export_format))

        return context