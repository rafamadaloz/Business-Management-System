from SGEO.apps.cadastro.models import Produto
from SGEO.apps.relatorios.tables import ProdutosTable
from SGEO.apps.base.custom_views import CustomListView
from django_tables2.export.views import ExportMixin
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView


class RelatorioProdutosView(ExportMixin, CustomListView):
    template_name = 'relatorios/produtos/geral.html'
    model = Produto
    table_class = ProdutosTable
    context_object_name = 'all_produtos'
    permission_codename = 'acessar_relatorio_produtos'

    def get_context_data(self, **kwargs):
        context = super(RelatorioProdutosView,
                        self).get_context_data(**kwargs)
        context['title_complete'] = 'Relatório de Produtos'
        context['mais_vendidos'] = self.model.objects.order_by('-quantidade_vendida')[:10]
        context['mais_vendidos'] = reversed(context['mais_vendidos'])

        context['menos_vendidos'] = self.model.objects.order_by('quantidade_vendida')[:10]
        context['menos_vendidos'] = reversed(context['menos_vendidos'])

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