# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F

from SGEO.apps.cadastro.models import Cliente, Fornecedor, Produto, Empresa, Transportadora
from SGEO.apps.vendas.models import OrcamentoVenda, PedidoVenda
from SGEO.apps.compras.models import OrcamentoCompra, PedidoCompra
from SGEO.apps.financeiro.models import MovimentoCaixa, Entrada, Saida
from SGEO.apps.fiscal.models import NotaFiscal, ConfiguracaoNotaFiscal
from SGEO.apps.boletos.models import ConfiguracaoBoleto
from SGEO.apps.contador.models import Contador
from django.db.models import Sum
from django.db import connection

from datetime import datetime
from calendar import monthrange


class BaseView(TemplateView):
    template_name = 'base/base.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        #if ConfiguracaoBoleto.objects.all()[0].exists():
            #context['configuracao_boleto'] = ConfiguracaoBoleto.objects.all()[0]
        context['configuracao_boleto'] = False


        return context


class IndexView(TemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        quantidade_cadastro = {}
        agenda_hoje = {}
        alertas = {}
        data_atual = datetime.now().date()

        nfes = NotaFiscal.objects.all()

        nro_notas_em_digitacao = 0
        nro_notas_autorizadas = 0
        nro_notas_canceladas = 0

        for nf in nfes:
            if nf.status_nfe == '3':
                nro_notas_em_digitacao += 1
            if nf.status_nfe == '1':
                nro_notas_autorizadas += 1
            if nf.status_nfe == '8':
                nro_notas_canceladas += 1

        nro_notas_restantes = 200 - nro_notas_autorizadas

        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_database_size('SGEO')")
            tamanho = cursor.fetchall()[0][0]
            context['armazenamento'] = round((tamanho / 1000000), 3)



        data_de_hoje = datetime.now().date()
        mes_atual = datetime.now().month
        ano_atual = datetime.now().year

        dias_do_mes = monthrange(ano_atual, mes_atual)[1]

        ultimo_dia_mes = datetime(ano_atual, mes_atual, dias_do_mes)
        primeiro_dia_mes = datetime(ano_atual, mes_atual, 1)

        a_receber_dia = Entrada.objects.filter(
            data_vencimento=datetime.now().date(),
            status__in=['1']
        )

        a_receber_mes = Entrada.objects.filter(
            data_vencimento__gte=data_de_hoje,
            data_vencimento__lte=ultimo_dia_mes,
            status__in=['1']
        )

        recebidos_dia = Entrada.objects.filter(
            data_vencimento=datetime.now().date(),
            status__in=['0']
        )

        recebidos_mes = Entrada.objects.filter(
            data_vencimento__lte=data_de_hoje,
            data_vencimento__gte=primeiro_dia_mes,
            status__in=['0']
        )

        pagamentos_dia = Saida.objects.filter(
            data_vencimento=datetime.now().date(),
            status__in=['0']
        )

        pagamentos_mes = Saida.objects.filter(
            data_vencimento__lte=data_de_hoje,
            data_vencimento__gte=primeiro_dia_mes,
            status__in=['0']
        )

        a_pagar_dia = Saida.objects.filter(
            data_vencimento=datetime.now().date(),
            status__in=['1']
        )

        a_pagar_mes = Saida.objects.filter(
            data_vencimento__gte=data_de_hoje,
            data_vencimento__lte=ultimo_dia_mes,
            status__in=['1']
        )


        context['valor_a_receber_dia'] = a_receber_dia.aggregate(soma_total=Sum('valor_liquido'))['soma_total']
        context['valor_a_receber_mes'] = a_receber_mes.aggregate(soma_total=Sum('valor_liquido'))['soma_total']

        context['valor_recebidos_dia'] = recebidos_dia.aggregate(soma_total=Sum('valor_liquido'))['soma_total']
        context['valor_recebidos_mes'] = recebidos_mes.aggregate(soma_total=Sum('valor_liquido'))['soma_total']

        context['valor_a_pagar_dia'] = a_pagar_dia.aggregate(soma_total=Sum('valor_liquido'))['soma_total']
        context['valor_a_pagar_mes'] = a_pagar_mes.aggregate(soma_total=Sum('valor_liquido'))['soma_total']

        context['valor_pago_dia'] = pagamentos_dia.aggregate(soma_total=Sum('valor_liquido'))['soma_total']
        context['valor_pago_mes'] = pagamentos_mes.aggregate(soma_total=Sum('valor_liquido'))['soma_total']

        context['todos_recebidos'] = MovimentoCaixa.objects.order_by('data_movimento').all()


        context['all_a_receber'] = Entrada.objects.filter(
            data_vencimento__gte=datetime.now().date(),
            status__in=['1']
        ).order_by('data_vencimento')[:7]

        context['qtd_a_receber'] = Entrada.objects.filter(
            data_vencimento__gte=datetime.now().date(),
            status__in=['1']
        ).count()

        context['all_a_pagar'] = Saida.objects.filter(
            data_vencimento__gte=datetime.now().date(),
            status__in=['1']
        ).order_by('data_vencimento')[:7]

        context['qtd_a_pagar'] = Saida.objects.filter(
            data_vencimento__gte=datetime.now().date(),
            status__in=['1']
        ).count()

        context['entradas_atrasadas'] = Entrada.objects.filter(
            data_vencimento__lt=datetime.now().date(),
            status__in=['1', '2']
        ).order_by('data_vencimento')[:7]

        context['pagamentos_atrasados'] = Saida.objects.filter(
            data_vencimento__lt=datetime.now().date(),
            status__in=['1', '2']
        ).order_by('data_vencimento')[:7]

        context['contador_nfe_em_digitacao'] = nro_notas_em_digitacao
        context['contador_nfe_autorizada'] = nro_notas_autorizadas
        context['contador_nfe_cancelada'] = nro_notas_canceladas
        context['contador_nfe_restantes'] = nro_notas_restantes
        context['contador_nfe_total'] = nfes.count()
        context['certificado_a1'] = ConfiguracaoNotaFiscal.arquivo_certificado_a1

        context['data_atual'] = data_atual.strftime('%d/%m/%Y')

        quantidade_cadastro['clientes'] = Cliente.objects.all().count()
        quantidade_cadastro['fornecedores'] = Fornecedor.objects.all().count()
        quantidade_cadastro['produtos'] = Produto.objects.all().count()
        #quantidade_cadastro['servicos'] = Servico.objects.all().count()
        quantidade_cadastro['empresas'] = Empresa.objects.all().count()
        quantidade_cadastro[
            'transportadoras'] = Transportadora.objects.all().count()
        context['quantidade_cadastro'] = quantidade_cadastro

        agenda_hoje['orcamento_venda_hoje'] = OrcamentoVenda.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['orcamento_compra_hoje'] = OrcamentoCompra.objects.filter(
            data_vencimento=data_atual, status='0').count()
        agenda_hoje['pedido_venda_hoje'] = PedidoVenda.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['pedido_compra_hoje'] = PedidoCompra.objects.filter(
            data_entrega=data_atual, status='0').count()
        agenda_hoje['contas_receber_hoje'] = Entrada.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        agenda_hoje['contas_pagar_hoje'] = Saida.objects.filter(
            data_vencimento=data_atual, status__in=['1', '2']).count()
        context['agenda_hoje'] = agenda_hoje

        alertas['produtos_baixo_estoque'] = Produto.objects.filter(
            estoque_atual__lte=F('estoque_minimo')).count()
        alertas['orcamentos_venda_vencidos'] = OrcamentoVenda.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_venda_atrasados'] = PedidoVenda.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['orcamentos_compra_vencidos'] = OrcamentoCompra.objects.filter(
            data_vencimento__lte=data_atual, status='0').count()
        alertas['pedidos_compra_atrasados'] = PedidoCompra.objects.filter(
            data_entrega__lte=data_atual, status='0').count()
        alertas['contas_receber_atrasadas'] = Entrada.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        alertas['contas_pagar_atrasadas'] = Saida.objects.filter(
            data_vencimento__lte=data_atual, status__in=['1', '2']).count()
        context['alertas'] = alertas

        try:
            context['movimento_dia'] = MovimentoCaixa.objects.get(
                data_movimento=data_atual)
        except (MovimentoCaixa.DoesNotExist, ObjectDoesNotExist):
            ultimo_mvmt = MovimentoCaixa.objects.filter(
                data_movimento__lt=data_atual)
            if ultimo_mvmt:
                context['saldo'] = ultimo_mvmt.latest(
                    'data_movimento').saldo_final
            else:
                context['saldo'] = '0,00'

        return context


def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
