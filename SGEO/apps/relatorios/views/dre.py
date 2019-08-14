from SGEO.apps.vendas.models import PedidoVenda
from SGEO.apps.financeiro.models import Entrada, Saida
from SGEO.apps.base.custom_views import CustomListView
from django_tables2.export.views import ExportMixin
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
from datetime import datetime


class DREView(CustomListView):
    template_name = 'relatorios/dre/geral.html'
    model = PedidoVenda
    context_object_name = 'all_vendas'
    permission_codename = 'acessar_relatorio_dre'

    def get_context_data(self, **kwargs):
        context = super(DREView,
                        self).get_context_data(**kwargs)

        context['title_complete'] = 'Demonstração do Resultado do Exercício - DRE'
        ano_atual = datetime.now().year

        vendas_faturadas = PedidoVenda.objects.filter(status='1')
        entradas = Entrada.objects.all()
        saidas = Saida.objects.all()

        despesas_com_vendas = saidas.filter(classificacao_dre='1')
        despesas_administrativas = saidas.filter(classificacao_dre='2')
        pro_labore = saidas.filter(classificacao_dre='3')
        despesas_financeiras = saidas.filter(classificacao_dre='4')
        outras_despesas = saidas.filter(classificacao_dre='5')

        receitas_financeiras = entradas.filter(classificacao_dre='3')
        outras_receitas = entradas.filter(classificacao_dre='4')

        def total_pro_labore_do_mes(mes, ano):
            pro_labores = pro_labore.filter(
                data_emissao__year=ano,
                data_emissao__month=mes,
            )
            total = 0
            for despesa in pro_labores:
                total += despesa.valor_liquido
            return total

        def total_receitas_financeiras_do_mes(mes, ano):
            receitas = receitas_financeiras.filter(
                data_emissao__year=ano,
                data_emissao__month=mes,
            )
            total = 0
            for receita in receitas:
                total += receita.valor_liquido
            return total

        def total_despesas_financeiras_do_mes(mes, ano):
            despesas = despesas_financeiras.filter(
                data_emissao__year=ano,
                data_emissao__month=mes,
            )
            total = 0
            for despesa in despesas:
                total += despesa.valor_liquido
            return total

        def total_outras_receitas_do_mes(mes, ano):
            receitas = outras_receitas.filter(
                data_emissao__year=ano,
                data_emissao__month=mes,
            )
            total = 0
            for receita in receitas:
                total += receita.valor_liquido
            return total

        def total_outras_despesas_do_mes(mes, ano):
            despesas = outras_despesas.filter(
                data_emissao__year=ano,
                data_emissao__month=mes,
            )
            total = 0
            for despesa in despesas:
                total += despesa.valor_liquido
            return total

        # RECEITA OPERACIONAL BRUTA #

        valor_vendas_produtos = 0

        for venda in vendas_faturadas:
            valor_vendas_produtos += venda.get_total_produtos()

        context['vendas_produtos_mercadorias'] = valor_vendas_produtos

        #JANEIRO

        vendas_faturadas_jan = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=1,
        )

        valor_vendas_produtos_jan = 0
        valor_abatimentos_jan = 0
        valor_impostos_jan = 0
        valor_custos_jan = 0
        for venda in vendas_faturadas_jan:
            valor_vendas_produtos_jan += venda.get_total_produtos()
            valor_abatimentos_jan += venda.get_valor_desconto_total()
            valor_impostos_jan += venda.impostos
            valor_custos_jan += venda.get_total_custo()


        despesas_com_vendas_jan_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=1,
        )

        valor_despesas_com_vendas_jan = 0
        for despesa in despesas_com_vendas_jan_obj:
            valor_despesas_com_vendas_jan += despesa.valor_liquido

        despesas_adm_jan_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=1,
        )

        valor_despesas_adm_jan = 0
        for despesa in despesas_adm_jan_obj:
            valor_despesas_adm_jan += despesa.valor_liquido

        context['vendas_produtos_mercadorias_jan'] = valor_vendas_produtos_jan
        context['abatimentos_jan'] = valor_abatimentos_jan
        context['impostos_jan'] = valor_impostos_jan
        context['deducoes_receita_bruta_jan'] = valor_abatimentos_jan + valor_impostos_jan
        context['receita_operacional_liquida_jan'] = valor_vendas_produtos_jan - context['deducoes_receita_bruta_jan']
        context['custos_jan'] = valor_custos_jan
        context['resultado_operacional_bruto_jan'] = context['receita_operacional_liquida_jan'] - valor_custos_jan
        if context['vendas_produtos_mercadorias_jan'] == 0:
            context['res_op_margem_jan'] = 0
        else:
            context['res_op_margem_jan'] = round((context['resultado_operacional_bruto_jan'] / context['vendas_produtos_mercadorias_jan'])*100, 2)
        context['despesas_com_vendas_jan'] = valor_despesas_com_vendas_jan
        context['despesas_adm_jan'] = valor_despesas_adm_jan
        context['despesas_prolabore_jan'] = total_pro_labore_do_mes(1, ano_atual)
        context['despesas_operacionais_jan'] = context['despesas_com_vendas_jan'] + context['despesas_adm_jan'] + context['despesas_prolabore_jan']
        context['receitas_financeiras_jan'] = total_receitas_financeiras_do_mes(1, ano_atual)
        context['despesas_financeiras_jan'] = total_despesas_financeiras_do_mes(1, ano_atual)
        context['despesas_receitas_fin_jan'] = context['receitas_financeiras_jan'] - context['despesas_financeiras_jan']
        context['outras_receitas_jan'] = total_receitas_financeiras_do_mes(1, ano_atual)
        context['outras_despesas_jan'] = total_despesas_financeiras_do_mes(1, ano_atual)
        context['outras_despesas_receitas_jan'] = context['outras_receitas_jan'] - context['outras_despesas_jan']
        context['res_op_antes_ir_csll_jan'] = context['resultado_operacional_bruto_jan'] - context['despesas_operacionais_jan'] + context['despesas_receitas_fin_jan'] + context['outras_despesas_receitas_jan']
        if context['vendas_produtos_mercadorias_jan'] == 0:
            context['margem_liquida_jan'] = 0
        else:
            context['margem_liquida_jan'] = round((context['res_op_antes_ir_csll_jan'] / context['vendas_produtos_mercadorias_jan'])*100, 2)

        #FEVEREIRO

        vendas_faturadas_fev = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=2,
        )
        valor_vendas_produtos_fev = 0
        valor_abatimentos_fev = 0
        valor_impostos_fev = 0
        valor_custos_fev = 0
        for venda in vendas_faturadas_fev:
            valor_vendas_produtos_fev += venda.get_total_produtos()
            valor_abatimentos_fev += venda.get_valor_desconto_total()
            valor_impostos_fev += venda.impostos
            valor_custos_fev += venda.get_total_custo()

        despesas_com_vendas_fev_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=2,
        )

        valor_despesas_com_vendas_fev = 0
        for despesa in despesas_com_vendas_fev_obj:
            valor_despesas_com_vendas_fev += despesa.valor_liquido

        despesas_adm_fev_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=2,
        )

        valor_despesas_adm_fev = 0
        for despesa in despesas_adm_fev_obj:
            valor_despesas_adm_fev += despesa.valor_liquido


        context['vendas_produtos_mercadorias_fev'] = valor_vendas_produtos_fev
        context['abatimentos_fev'] = valor_abatimentos_fev
        context['impostos_fev'] = valor_impostos_fev
        context['deducoes_receita_bruta_fev'] = valor_abatimentos_fev + valor_impostos_fev
        context['receita_operacional_liquida_fev'] = valor_vendas_produtos_fev - context['deducoes_receita_bruta_fev']
        context['custos_fev'] = valor_custos_fev
        context['resultado_operacional_bruto_fev'] = context['receita_operacional_liquida_fev'] - valor_custos_fev
        if context['vendas_produtos_mercadorias_fev'] == 0:
            context['res_op_margem_fev'] = 0
        else:
            context['res_op_margem_fev'] = round((context['resultado_operacional_bruto_fev'] / context['vendas_produtos_mercadorias_fev'])*100, 2)
        context['despesas_com_vendas_fev'] = valor_despesas_com_vendas_fev
        context['despesas_adm_fev'] = valor_despesas_adm_fev
        context['despesas_prolabore_fev'] = total_pro_labore_do_mes(2, ano_atual)
        context['despesas_operacionais_fev'] = context['despesas_com_vendas_fev'] + context['despesas_adm_fev'] + context['despesas_prolabore_fev']
        context['receitas_financeiras_fev'] = total_receitas_financeiras_do_mes(2, ano_atual)
        context['despesas_financeiras_fev'] = total_despesas_financeiras_do_mes(2, ano_atual)
        context['despesas_receitas_fin_fev'] = context['receitas_financeiras_fev'] - context['despesas_financeiras_fev']
        context['outras_receitas_fev'] = total_receitas_financeiras_do_mes(2, ano_atual)
        context['outras_despesas_fev'] = total_despesas_financeiras_do_mes(2, ano_atual)
        context['outras_despesas_receitas_fev'] = context['outras_receitas_fev'] - context['outras_despesas_fev']
        context['res_op_antes_ir_csll_fev'] = context['resultado_operacional_bruto_fev'] - context['despesas_operacionais_fev'] + context['despesas_receitas_fin_fev'] + context['outras_despesas_receitas_fev']
        if context['vendas_produtos_mercadorias_fev'] == 0:
            context['margem_liquida_fev'] = 0
        else:
            context['margem_liquida_fev'] = round((context['res_op_antes_ir_csll_fev'] / context['vendas_produtos_mercadorias_fev'])*100, 2)

        #MARÇO

        vendas_faturadas_mar = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=3,
        )

        valor_vendas_produtos_mar = 0
        valor_abatimentos_mar = 0
        valor_impostos_mar = 0
        valor_custos_mar = 0
        for venda in vendas_faturadas_mar:
            valor_vendas_produtos_mar += venda.get_total_produtos()
            valor_abatimentos_mar += venda.get_valor_desconto_total()
            valor_impostos_mar += venda.impostos
            valor_custos_mar += venda.get_total_custo()

        despesas_com_vendas_mar_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=3,
        )

        valor_despesas_com_vendas_mar = 0
        for despesa in despesas_com_vendas_mar_obj:
            valor_despesas_com_vendas_mar += despesa.valor_liquido

        despesas_adm_mar_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=3,
        )

        valor_despesas_adm_mar= 0
        for despesa in despesas_adm_mar_obj:
            valor_despesas_adm_mar += despesa.valor_liquido

        context['vendas_produtos_mercadorias_mar'] = valor_vendas_produtos_mar
        context['abatimentos_mar'] = valor_abatimentos_mar
        context['impostos_mar'] = valor_impostos_mar
        context['deducoes_receita_bruta_mar'] = valor_abatimentos_mar + valor_impostos_mar
        context['receita_operacional_liquida_mar'] = valor_vendas_produtos_mar - context['deducoes_receita_bruta_mar']
        context['custos_mar'] = valor_custos_mar
        context['resultado_operacional_bruto_mar'] = context['receita_operacional_liquida_mar'] - valor_custos_mar
        if context['vendas_produtos_mercadorias_mar'] == 0:
            context['res_op_margem_mar'] = 0
        else:
            context['res_op_margem_mar'] = round((context['resultado_operacional_bruto_mar'] / context['vendas_produtos_mercadorias_mar'])*100, 2)
        context['despesas_com_vendas_mar'] = valor_despesas_com_vendas_mar
        context['despesas_adm_mar'] = valor_despesas_adm_mar
        context['despesas_prolabore_mar'] = total_pro_labore_do_mes(3, ano_atual)
        context['despesas_operacionais_mar'] = context['despesas_com_vendas_mar'] + context['despesas_adm_mar'] + context['despesas_prolabore_mar']
        context['receitas_financeiras_mar'] = total_receitas_financeiras_do_mes(3, ano_atual)
        context['despesas_financeiras_mar'] = total_despesas_financeiras_do_mes(3, ano_atual)
        context['despesas_receitas_fin_mar'] = context['receitas_financeiras_mar'] - context['despesas_financeiras_mar']
        context['outras_receitas_mar'] = total_receitas_financeiras_do_mes(3, ano_atual)
        context['outras_despesas_mar'] = total_despesas_financeiras_do_mes(3, ano_atual)
        context['outras_despesas_receitas_mar'] = context['outras_receitas_mar'] - context['outras_despesas_mar']
        context['res_op_antes_ir_csll_mar'] = context['resultado_operacional_bruto_mar'] - context['despesas_operacionais_mar'] + context['despesas_receitas_fin_mar'] + context['outras_despesas_receitas_mar']
        if context['vendas_produtos_mercadorias_mar'] == 0:
            context['margem_liquida_mar'] = 0
        else:
            context['margem_liquida_mar'] = round((context['res_op_antes_ir_csll_mar'] / context['vendas_produtos_mercadorias_mar'])*100, 2)

        #ABRIL

        vendas_faturadas_abr = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=4,
        )

        valor_vendas_produtos_abr = 0
        valor_abatimentos_abr = 0
        valor_impostos_abr = 0
        valor_custos_abr = 0
        for venda in vendas_faturadas_abr:
            valor_vendas_produtos_abr += venda.get_total_produtos()
            valor_abatimentos_abr += venda.get_valor_desconto_total()
            valor_impostos_abr += venda.impostos
            valor_custos_abr += venda.get_total_custo()

        despesas_com_vendas_abr_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=4,
        )

        valor_despesas_com_vendas_abr = 0
        for despesa in despesas_com_vendas_abr_obj:
            valor_despesas_com_vendas_abr += despesa.valor_liquido

        despesas_adm_abr_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=4,
        )

        valor_despesas_adm_abr = 0
        for despesa in despesas_adm_abr_obj:
            valor_despesas_adm_abr += despesa.valor_liquido

        context['vendas_produtos_mercadorias_abr'] = valor_vendas_produtos_abr
        context['abatimentos_abr'] = valor_abatimentos_abr
        context['impostos_abr'] = valor_impostos_abr
        context['deducoes_receita_bruta_abr'] = valor_abatimentos_abr + valor_impostos_abr
        context['receita_operacional_liquida_abr'] = valor_vendas_produtos_abr - context['deducoes_receita_bruta_abr']
        context['custos_abr'] = valor_custos_abr
        context['resultado_operacional_bruto_abr'] = context['receita_operacional_liquida_abr'] - valor_custos_abr
        if context['vendas_produtos_mercadorias_abr'] == 0:
            context['res_op_margem_abr'] = 0
        else:
            context['res_op_margem_abr'] = round((context['resultado_operacional_bruto_abr'] / context['vendas_produtos_mercadorias_abr'])*100, 2)
        context['despesas_com_vendas_abr'] = valor_despesas_com_vendas_abr
        context['despesas_adm_abr'] = valor_despesas_adm_abr
        context['despesas_prolabore_abr'] = total_pro_labore_do_mes(4, ano_atual)
        context['despesas_operacionais_abr'] = context['despesas_com_vendas_abr'] + context['despesas_adm_abr'] + context['despesas_prolabore_abr']
        context['receitas_financeiras_abr'] = total_receitas_financeiras_do_mes(4, ano_atual)
        context['despesas_financeiras_abr'] = total_despesas_financeiras_do_mes(4, ano_atual)
        context['despesas_receitas_fin_abr'] = context['receitas_financeiras_abr'] - context['despesas_financeiras_abr']
        context['outras_receitas_abr'] = total_receitas_financeiras_do_mes(4, ano_atual)
        context['outras_despesas_abr'] = total_despesas_financeiras_do_mes(4, ano_atual)
        context['outras_despesas_receitas_abr'] = context['outras_receitas_abr'] - context['outras_despesas_abr']
        context['res_op_antes_ir_csll_abr'] = context['resultado_operacional_bruto_abr'] - context['despesas_operacionais_abr'] + context['despesas_receitas_fin_abr'] + context['outras_despesas_receitas_abr']
        if context['vendas_produtos_mercadorias_abr'] == 0:
            context['margem_liquida_abr'] = 0
        else:
            context['margem_liquida_abr'] = round((context['res_op_antes_ir_csll_abr'] / context['vendas_produtos_mercadorias_abr'])*100, 2)

        #MAIO

        vendas_faturadas_mai = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=5,
        )

        valor_vendas_produtos_mai = 0
        valor_abatimentos_mai = 0
        valor_impostos_mai = 0
        valor_custos_mai = 0
        for venda in vendas_faturadas_mai:
            valor_vendas_produtos_mai += venda.get_total_produtos()
            valor_abatimentos_mai += venda.get_valor_desconto_total()
            valor_impostos_mai += venda.impostos
            valor_custos_mai += venda.get_total_custo()

        despesas_com_vendas_mai_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=5,
        )

        valor_despesas_com_vendas_mai = 0
        for despesa in despesas_com_vendas_mai_obj:
            valor_despesas_com_vendas_mai += despesa.valor_liquido

        despesas_adm_mai_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=5,
        )

        valor_despesas_adm_mai = 0
        for despesa in despesas_adm_mai_obj:
            valor_despesas_adm_mai += despesa.valor_liquido

        context['vendas_produtos_mercadorias_mai'] = valor_vendas_produtos_mai
        context['abatimentos_mai'] = valor_abatimentos_mai
        context['impostos_mai'] = valor_impostos_mai
        context['deducoes_receita_bruta_mai'] = valor_abatimentos_mai + valor_impostos_mai
        context['receita_operacional_liquida_mai'] = valor_vendas_produtos_mai - context['deducoes_receita_bruta_mai']
        context['custos_mai'] = valor_custos_mai
        context['resultado_operacional_bruto_mai'] = context['receita_operacional_liquida_mai'] - valor_custos_mai
        if context['vendas_produtos_mercadorias_mai'] == 0:
            context['res_op_margem_mai'] = 0
        else:
            context['res_op_margem_mai'] = round((context['resultado_operacional_bruto_mai'] / context['vendas_produtos_mercadorias_mai'])*100, 2)
        context['despesas_com_vendas_mai'] = valor_despesas_com_vendas_mai
        context['despesas_adm_mai'] = valor_despesas_adm_mai
        context['despesas_prolabore_mai'] = total_pro_labore_do_mes(5, ano_atual)
        context['despesas_operacionais_mai'] = context['despesas_com_vendas_mai'] + context['despesas_adm_mai'] + context['despesas_prolabore_mai']
        context['receitas_financeiras_mai'] = total_receitas_financeiras_do_mes(5, ano_atual)
        context['despesas_financeiras_mai'] = total_despesas_financeiras_do_mes(5, ano_atual)
        context['despesas_receitas_fin_mai'] = context['receitas_financeiras_mai'] - context['despesas_financeiras_mai']
        context['outras_receitas_mai'] = total_receitas_financeiras_do_mes(5, ano_atual)
        context['outras_despesas_mai'] = total_despesas_financeiras_do_mes(5, ano_atual)
        context['outras_despesas_receitas_mai'] = context['outras_receitas_mai'] - context['outras_despesas_mai']
        context['res_op_antes_ir_csll_mai'] = context['resultado_operacional_bruto_mai'] - context['despesas_operacionais_mai'] + context['despesas_receitas_fin_mai'] + context['outras_despesas_receitas_mai']
        if context['vendas_produtos_mercadorias_mai'] == 0:
            context['margem_liquida_mai'] = 0
        else:
            context['margem_liquida_mai'] = round((context['res_op_antes_ir_csll_mai'] / context['vendas_produtos_mercadorias_mai'])*100, 2)

        #JUNHO

        vendas_faturadas_jun = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=6,
        )

        valor_vendas_produtos_jun = 0
        valor_abatimentos_jun = 0
        valor_impostos_jun = 0
        valor_custos_jun = 0
        for venda in vendas_faturadas_jun:
            valor_vendas_produtos_jun += venda.get_total_produtos()
            valor_abatimentos_jun += venda.get_valor_desconto_total()
            valor_impostos_jun += venda.impostos
            valor_custos_jun += venda.get_total_custo()

        despesas_com_vendas_jun_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=6,
        )

        valor_despesas_com_vendas_jun = 0
        for despesa in despesas_com_vendas_jun_obj:
            valor_despesas_com_vendas_jun += despesa.valor_liquido

        despesas_adm_jun_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=6,
        )

        valor_despesas_adm_jun = 0
        for despesa in despesas_adm_jun_obj:
            valor_despesas_adm_jun += despesa.valor_liquido

        context['vendas_produtos_mercadorias_jun'] = valor_vendas_produtos_jun
        context['abatimentos_jun'] = valor_abatimentos_jun
        context['impostos_jun'] = valor_impostos_jun
        context['deducoes_receita_bruta_jun'] = valor_abatimentos_jun + valor_impostos_jun
        context['receita_operacional_liquida_jun'] = valor_vendas_produtos_jun - context['deducoes_receita_bruta_jun']
        context['custos_jun'] = valor_custos_jun
        context['resultado_operacional_bruto_jun'] = context['receita_operacional_liquida_jun'] - valor_custos_jun
        if context['vendas_produtos_mercadorias_jun'] == 0:
            context['res_op_margem_jun'] = 0
        else:
            context['res_op_margem_jun'] = round((context['resultado_operacional_bruto_jun'] / context['vendas_produtos_mercadorias_jun'])*100, 2)
        context['despesas_com_vendas_jun'] = valor_despesas_com_vendas_jun
        context['despesas_adm_jun'] = valor_despesas_adm_jun
        context['despesas_prolabore_jun'] = total_pro_labore_do_mes(6, ano_atual)
        context['despesas_operacionais_jun'] = context['despesas_com_vendas_jun'] + context['despesas_adm_jun'] + context['despesas_prolabore_jun']
        context['receitas_financeiras_jun'] = total_receitas_financeiras_do_mes(6, ano_atual)
        context['despesas_financeiras_jun'] = total_despesas_financeiras_do_mes(6, ano_atual)
        context['despesas_receitas_fin_jun'] = context['receitas_financeiras_jun'] - context['despesas_financeiras_jun']
        context['outras_receitas_jun'] = total_receitas_financeiras_do_mes(6, ano_atual)
        context['outras_despesas_jun'] = total_despesas_financeiras_do_mes(6, ano_atual)
        context['outras_despesas_receitas_jun'] = context['outras_receitas_jun'] - context['outras_despesas_jun']
        context['res_op_antes_ir_csll_jun'] = context['resultado_operacional_bruto_jun'] - context['despesas_operacionais_jun'] + context['despesas_receitas_fin_jun'] + context['outras_despesas_receitas_jun']
        if context['vendas_produtos_mercadorias_jun'] == 0:
            context['margem_liquida_jun'] = 0
        else:
            context['margem_liquida_jun'] = round((context['res_op_antes_ir_csll_jun'] / context['vendas_produtos_mercadorias_jun'])*100, 2)
        #JULHO

        vendas_faturadas_jul = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=7,
        )

        valor_vendas_produtos_jul = 0
        valor_abatimentos_jul = 0
        valor_impostos_jul = 0
        valor_custos_jul = 0
        for venda in vendas_faturadas_jul:
            valor_vendas_produtos_jul += venda.get_total_produtos()
            valor_abatimentos_jul += venda.get_valor_desconto_total()
            valor_impostos_jul += venda.impostos
            valor_custos_jul += venda.get_total_custo()

        despesas_com_vendas_jul_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=7,
        )

        valor_despesas_com_vendas_jul = 0
        for despesa in despesas_com_vendas_jul_obj:
            valor_despesas_com_vendas_jul += despesa.valor_liquido

        despesas_adm_jul_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=7,
        )

        valor_despesas_adm_jul = 0
        for despesa in despesas_adm_jul_obj:
            valor_despesas_adm_jul += despesa.valor_liquido

        context['vendas_produtos_mercadorias_jul'] = valor_vendas_produtos_jul
        context['abatimentos_jul'] = valor_abatimentos_jul
        context['impostos_jul'] = valor_impostos_jul
        context['deducoes_receita_bruta_jul'] = valor_abatimentos_jul + valor_impostos_jul
        context['receita_operacional_liquida_jul'] = valor_vendas_produtos_jul - context['deducoes_receita_bruta_jul']
        context['custos_jul'] = valor_custos_jul
        context['resultado_operacional_bruto_jul'] = context['receita_operacional_liquida_jul'] - valor_custos_jul
        if context['vendas_produtos_mercadorias_jul'] == 0:
            context['res_op_margem_jul'] = 0
        else:
            context['res_op_margem_jul'] = round((context['resultado_operacional_bruto_jul'] / context['vendas_produtos_mercadorias_jul'])*100, 2)
        context['despesas_com_vendas_jul'] = valor_despesas_com_vendas_jul
        context['despesas_adm_jul'] = valor_despesas_adm_jul
        context['despesas_prolabore_jul'] = total_pro_labore_do_mes(7, ano_atual)
        context['despesas_operacionais_jul'] = context['despesas_com_vendas_jul'] + context['despesas_adm_jul'] + context['despesas_prolabore_jul']
        context['receitas_financeiras_jul'] = total_receitas_financeiras_do_mes(7, ano_atual)
        context['despesas_financeiras_jul'] = total_despesas_financeiras_do_mes(7, ano_atual)
        context['despesas_receitas_fin_jul'] = context['receitas_financeiras_jul'] - context['despesas_financeiras_jul']
        context['outras_receitas_jul'] = total_receitas_financeiras_do_mes(7, ano_atual)
        context['outras_despesas_jul'] = total_despesas_financeiras_do_mes(7, ano_atual)
        context['outras_despesas_receitas_jul'] = context['outras_receitas_jul'] - context['outras_despesas_jul']
        context['res_op_antes_ir_csll_jul'] = context['resultado_operacional_bruto_jul'] - context['despesas_operacionais_jul'] + context['despesas_receitas_fin_jul'] + context['outras_despesas_receitas_jul']
        if context['vendas_produtos_mercadorias_jul'] == 0:
            context['margem_liquida_jul'] = 0
        else:
            context['margem_liquida_jul'] = round((context['res_op_antes_ir_csll_jul'] / context['vendas_produtos_mercadorias_jul'])*100, 2)

        #AGOSTO

        vendas_faturadas_ago = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=8,
        )

        valor_vendas_produtos_ago = 0
        valor_abatimentos_ago = 0
        valor_impostos_ago = 0
        valor_custos_ago = 0
        for venda in vendas_faturadas_ago:
            valor_vendas_produtos_ago += venda.get_total_produtos()
            valor_abatimentos_ago += venda.get_valor_desconto_total()
            valor_impostos_ago += venda.impostos
            valor_custos_ago += venda.get_total_custo()

        despesas_com_vendas_ago_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=8,
        )

        valor_despesas_com_vendas_ago = 0
        for despesa in despesas_com_vendas_ago_obj:
            valor_despesas_com_vendas_ago += despesa.valor_liquido

        despesas_adm_ago_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=8,
        )

        valor_despesas_adm_ago = 0
        for despesa in despesas_adm_ago_obj:
            valor_despesas_adm_ago += despesa.valor_liquido

        context['vendas_produtos_mercadorias_ago'] = valor_vendas_produtos_ago
        context['abatimentos_ago'] = valor_abatimentos_ago
        context['impostos_ago'] = valor_impostos_ago
        context['deducoes_receita_bruta_ago'] = valor_abatimentos_ago + valor_impostos_ago
        context['receita_operacional_liquida_ago'] = valor_vendas_produtos_ago - context['deducoes_receita_bruta_ago']
        context['custos_ago'] = valor_custos_ago
        context['resultado_operacional_bruto_ago'] = context['receita_operacional_liquida_ago'] - valor_custos_ago
        if context['vendas_produtos_mercadorias_ago'] == 0:
            context['res_op_margem_ago'] = 0
        else:
            context['res_op_margem_ago'] = round((context['resultado_operacional_bruto_ago'] / context['vendas_produtos_mercadorias_ago'])*100, 2)
        context['despesas_com_vendas_ago'] = valor_despesas_com_vendas_ago
        context['despesas_adm_ago'] = valor_despesas_adm_ago
        context['despesas_prolabore_ago'] = total_pro_labore_do_mes(8, ano_atual)
        context['despesas_operacionais_ago'] = context['despesas_com_vendas_ago'] + context['despesas_adm_ago'] + context['despesas_prolabore_ago']
        context['receitas_financeiras_ago'] = total_receitas_financeiras_do_mes(8, ano_atual)
        context['despesas_financeiras_ago'] = total_despesas_financeiras_do_mes(8, ano_atual)
        context['despesas_receitas_fin_ago'] = context['receitas_financeiras_ago'] - context['despesas_financeiras_ago']
        context['outras_receitas_ago'] = total_receitas_financeiras_do_mes(8, ano_atual)
        context['outras_despesas_ago'] = total_despesas_financeiras_do_mes(8, ano_atual)
        context['outras_despesas_receitas_ago'] = context['outras_receitas_ago'] - context['outras_despesas_ago']
        context['res_op_antes_ir_csll_ago'] = context['resultado_operacional_bruto_ago'] - context['despesas_operacionais_ago'] + context['despesas_receitas_fin_ago'] + context['outras_despesas_receitas_ago']
        if context['vendas_produtos_mercadorias_ago'] == 0:
            context['margem_liquida_ago'] = 0
        else:
            context['margem_liquida_ago'] = round((context['res_op_antes_ir_csll_ago'] / context['vendas_produtos_mercadorias_ago'])*100, 2)
        #SETEMBRO

        vendas_faturadas_set = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=9,
        )
        valor_vendas_produtos_set = 0
        valor_abatimentos_set = 0
        valor_impostos_set = 0
        valor_custos_set = 0
        for venda in vendas_faturadas_set:
            valor_vendas_produtos_set += venda.get_total_produtos()
            valor_abatimentos_set += venda.get_valor_desconto_total()
            valor_impostos_set += venda.impostos
            valor_custos_set += venda.get_total_custo()

        despesas_com_vendas_set_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=9,
        )

        valor_despesas_com_vendas_set = 0
        for despesa in despesas_com_vendas_set_obj:
            valor_despesas_com_vendas_set += despesa.valor_liquido

        despesas_adm_set_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=9,
        )

        valor_despesas_adm_set = 0
        for despesa in despesas_adm_set_obj:
            valor_despesas_adm_set += despesa.valor_liquido

        context['vendas_produtos_mercadorias_set'] = valor_vendas_produtos_set
        context['abatimentos_set'] = valor_abatimentos_set
        context['impostos_set'] = valor_impostos_set
        context['deducoes_receita_bruta_set'] = valor_abatimentos_set + valor_impostos_set
        context['receita_operacional_liquida_set'] = valor_vendas_produtos_set - context['deducoes_receita_bruta_set']
        context['custos_set'] = valor_custos_set
        context['resultado_operacional_bruto_set'] = context['receita_operacional_liquida_set'] - valor_custos_set
        if context['vendas_produtos_mercadorias_set'] == 0:
            context['res_op_margem_set'] = 0
        else:
            context['res_op_margem_set'] = round((context['resultado_operacional_bruto_set'] / context['vendas_produtos_mercadorias_set'])*100, 2)
        context['despesas_com_vendas_set'] = valor_despesas_com_vendas_set
        context['despesas_adm_set'] = valor_despesas_adm_set
        context['despesas_prolabore_set'] = total_pro_labore_do_mes(9, ano_atual)
        context['despesas_operacionais_set'] = context['despesas_com_vendas_set'] + context['despesas_adm_set'] + context['despesas_prolabore_set']
        context['receitas_financeiras_set'] = total_receitas_financeiras_do_mes(9, ano_atual)
        context['despesas_financeiras_set'] = total_despesas_financeiras_do_mes(9, ano_atual)
        context['despesas_receitas_fin_set'] = context['receitas_financeiras_set'] - context['despesas_financeiras_set']
        context['outras_receitas_set'] = total_receitas_financeiras_do_mes(9, ano_atual)
        context['outras_despesas_set'] = total_despesas_financeiras_do_mes(9, ano_atual)
        context['outras_despesas_receitas_set'] = context['outras_receitas_set'] - context['outras_despesas_set']
        context['res_op_antes_ir_csll_set'] = context['resultado_operacional_bruto_set'] - context['despesas_operacionais_set'] + context['despesas_receitas_fin_set'] + context['outras_despesas_receitas_set']
        if context['vendas_produtos_mercadorias_set'] == 0:
            context['margem_liquida_set'] = 0
        else:
            context['margem_liquida_set'] = round((context['res_op_antes_ir_csll_set'] / context['vendas_produtos_mercadorias_set'])*100, 2)
        #OUTUBRO

        vendas_faturadas_out = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=10,
        )

        valor_vendas_produtos_out = 0
        valor_abatimentos_out = 0
        valor_impostos_out = 0
        valor_custos_out = 0
        for venda in vendas_faturadas_out:
            valor_vendas_produtos_out += venda.get_total_produtos()
            valor_abatimentos_out += venda.get_valor_desconto_total()
            valor_impostos_out += venda.impostos
            valor_custos_out += venda.get_total_custo()

        despesas_com_vendas_out_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=10,
        )

        valor_despesas_com_vendas_out = 0
        for despesa in despesas_com_vendas_out_obj:
            valor_despesas_com_vendas_out += despesa.valor_liquido

        despesas_adm_out_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=10,
        )

        valor_despesas_adm_out = 0
        for despesa in despesas_adm_out_obj:
            valor_despesas_adm_out += despesa.valor_liquido

        context['vendas_produtos_mercadorias_out'] = valor_vendas_produtos_out
        context['abatimentos_out'] = valor_abatimentos_out
        context['impostos_out'] = valor_impostos_out
        context['deducoes_receita_bruta_out'] = valor_abatimentos_out + valor_impostos_out
        context['receita_operacional_liquida_out'] = valor_vendas_produtos_out - context['deducoes_receita_bruta_out']
        context['custos_out'] = valor_custos_out
        context['resultado_operacional_bruto_out'] = context['receita_operacional_liquida_out'] - valor_custos_out
        if context['vendas_produtos_mercadorias_out'] == 0:
            context['res_op_margem_out'] = 0
        else:
            context['res_op_margem_out'] = round((context['resultado_operacional_bruto_out'] / context['vendas_produtos_mercadorias_out'])*100, 2)
        context['despesas_com_vendas_out'] = valor_despesas_com_vendas_out
        context['despesas_adm_out'] = valor_despesas_adm_out
        context['despesas_prolabore_out'] = total_pro_labore_do_mes(10, ano_atual)
        context['despesas_operacionais_out'] = context['despesas_com_vendas_out'] + context['despesas_adm_out'] + context['despesas_prolabore_out']
        context['receitas_financeiras_out'] = total_receitas_financeiras_do_mes(10, ano_atual)
        context['despesas_financeiras_out'] = total_despesas_financeiras_do_mes(10, ano_atual)
        context['despesas_receitas_fin_out'] = context['receitas_financeiras_out'] - context['despesas_financeiras_out']
        context['outras_receitas_out'] = total_receitas_financeiras_do_mes(10, ano_atual)
        context['outras_despesas_out'] = total_despesas_financeiras_do_mes(10, ano_atual)
        context['outras_despesas_receitas_out'] = context['outras_receitas_out'] - context['outras_despesas_out']
        context['res_op_antes_ir_csll_out'] = context['resultado_operacional_bruto_out'] - context['despesas_operacionais_out'] + context['despesas_receitas_fin_out'] + context['outras_despesas_receitas_out']
        if context['vendas_produtos_mercadorias_out'] == 0:
            context['margem_liquida_out'] = 0
        else:
            context['margem_liquida_out'] = round((context['res_op_antes_ir_csll_out'] / context['vendas_produtos_mercadorias_out'])*100, 2)
        #NOVEMBRO

        vendas_faturadas_nov = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=11,
        )

        valor_vendas_produtos_nov = 0
        valor_abatimentos_nov = 0
        valor_impostos_nov = 0
        valor_custos_nov = 0
        for venda in vendas_faturadas_nov:
            valor_vendas_produtos_nov += venda.get_total_produtos()
            valor_abatimentos_nov += venda.get_valor_desconto_total()
            valor_impostos_nov += venda.impostos
            valor_custos_nov += venda.get_total_custo()

        despesas_com_vendas_nov_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=11,
        )

        valor_despesas_com_vendas_nov = 0
        for despesa in despesas_com_vendas_nov_obj:
            valor_despesas_com_vendas_nov += despesa.valor_liquido

        despesas_adm_nov_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=11,
        )

        valor_despesas_adm_nov = 0
        for despesa in despesas_adm_nov_obj:
            valor_despesas_adm_nov += despesa.valor_liquido

        context['vendas_produtos_mercadorias_nov'] = valor_vendas_produtos_nov
        context['abatimentos_nov'] = valor_abatimentos_nov
        context['impostos_nov'] = valor_impostos_nov
        context['deducoes_receita_bruta_nov'] = valor_abatimentos_nov + valor_impostos_nov
        context['receita_operacional_liquida_nov'] = valor_vendas_produtos_nov - context['deducoes_receita_bruta_nov']
        context['custos_nov'] = valor_custos_nov
        context['resultado_operacional_bruto_nov'] = context['receita_operacional_liquida_nov'] - valor_custos_nov
        if context['vendas_produtos_mercadorias_nov'] == 0:
            context['res_op_margem_nov'] = 0
        else:
            context['res_op_margem_nov'] = round((context['resultado_operacional_bruto_nov'] / context['vendas_produtos_mercadorias_nov'])*100, 2)
        context['despesas_com_vendas_nov'] = valor_despesas_com_vendas_nov
        context['despesas_adm_nov'] = valor_despesas_adm_nov
        context['despesas_prolabore_nov'] = total_pro_labore_do_mes(9, ano_atual)
        context['despesas_operacionais_nov'] = context['despesas_com_vendas_nov'] + context['despesas_adm_nov'] + context['despesas_prolabore_nov']
        context['receitas_financeiras_nov'] = total_receitas_financeiras_do_mes(11, ano_atual)
        context['despesas_financeiras_nov'] = total_despesas_financeiras_do_mes(11, ano_atual)
        context['despesas_receitas_fin_nov'] = context['receitas_financeiras_nov'] - context['despesas_financeiras_nov']
        context['outras_receitas_nov'] = total_receitas_financeiras_do_mes(11, ano_atual)
        context['outras_despesas_nov'] = total_despesas_financeiras_do_mes(11, ano_atual)
        context['outras_despesas_receitas_nov'] = context['outras_receitas_nov'] - context['outras_despesas_nov']
        context['res_op_antes_ir_csll_nov'] = context['resultado_operacional_bruto_nov'] - context['despesas_operacionais_nov'] + context['despesas_receitas_fin_nov'] + context['outras_despesas_receitas_nov']
        if context['vendas_produtos_mercadorias_nov'] == 0:
            context['margem_liquida_nov'] = 0
        else:
            context['margem_liquida_nov'] = round((context['res_op_antes_ir_csll_nov'] / context['vendas_produtos_mercadorias_nov'])*100, 2)
        #DEZEMBRO

        vendas_faturadas_dez = vendas_faturadas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=12,
        )
        valor_vendas_produtos_dez = 0
        valor_abatimentos_dez = 0
        valor_impostos_dez = 0
        valor_custos_dez = 0
        for venda in vendas_faturadas_dez:
            valor_vendas_produtos_dez += venda.get_total_produtos()
            valor_abatimentos_dez += venda.get_valor_desconto_total()
            valor_impostos_dez += venda.impostos
            valor_custos_dez += venda.get_total_custo()

        despesas_com_vendas_dez_obj = despesas_com_vendas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=12,
        )

        valor_despesas_com_vendas_dez = 0
        for despesa in despesas_com_vendas_dez_obj:
            valor_despesas_com_vendas_dez += despesa.valor_liquido

        despesas_adm_dez_obj = despesas_administrativas.filter(
            data_emissao__year=ano_atual,
            data_emissao__month=12,
        )

        valor_despesas_adm_dez = 0
        for despesa in despesas_adm_dez_obj:
            valor_despesas_adm_dez += despesa.valor_liquido

        context['vendas_produtos_mercadorias_dez'] = valor_vendas_produtos_dez
        context['abatimentos_dez'] = valor_abatimentos_dez
        context['impostos_dez'] = valor_impostos_dez
        context['deducoes_receita_bruta_dez'] = valor_abatimentos_dez + valor_impostos_dez
        context['receita_operacional_liquida_dez'] = valor_vendas_produtos_dez - context['deducoes_receita_bruta_dez']
        context['custos_dez'] = valor_custos_dez
        context['resultado_operacional_bruto_dez'] = context['receita_operacional_liquida_dez'] - valor_custos_dez
        if context['vendas_produtos_mercadorias_dez'] == 0:
            context['res_op_margem_dez'] = 0
        else:
            context['res_op_margem_dez'] = round((context['resultado_operacional_bruto_dez'] / context['vendas_produtos_mercadorias_dez'])*100, 2)
        context['despesas_com_vendas_dez'] = valor_despesas_com_vendas_dez
        context['despesas_adm_dez'] = valor_despesas_adm_dez
        context['despesas_prolabore_dez'] = total_pro_labore_do_mes(12, ano_atual)
        context['despesas_operacionais_dez'] = context['despesas_com_vendas_dez'] + context['despesas_adm_dez'] + context['despesas_prolabore_dez']
        context['receitas_financeiras_dez'] = total_receitas_financeiras_do_mes(12, ano_atual)
        context['despesas_financeiras_dez'] = total_despesas_financeiras_do_mes(12, ano_atual)
        context['despesas_receitas_fin_dez'] = context['receitas_financeiras_dez'] - context['despesas_financeiras_dez']
        context['outras_receitas_dez'] = total_receitas_financeiras_do_mes(12, ano_atual)
        context['outras_despesas_dez'] = total_despesas_financeiras_do_mes(12, ano_atual)
        context['outras_despesas_receitas_dez'] = context['outras_receitas_dez'] - context['outras_despesas_dez']
        context['res_op_antes_ir_csll_dez'] = context['resultado_operacional_bruto_dez'] - context['despesas_operacionais_dez'] + context['despesas_receitas_fin_dez'] + context['outras_despesas_receitas_dez']
        if context['vendas_produtos_mercadorias_dez'] == 0:
            context['margem_liquida_dez'] = 0
        else:
            context['margem_liquida_dez'] = round((context['res_op_antes_ir_csll_dez'] / context['vendas_produtos_mercadorias_dez'])*100, 2)
        # FIM RECEITA OPERACIONAL BRUTA #

        return context

