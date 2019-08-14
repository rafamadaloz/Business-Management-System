# tutorial/tables.py
import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable
from SGEO.apps.cadastro.models import Cliente, Produto
from SGEO.apps.financeiro.models import Entrada
from SGEO.apps.vendas.models import PedidoVenda
from django.db.models.functions import Length


class ClienteTable(ColumnShiftTable):
    export_formats = ['csv', 'xlsx']

    cpf = tables.Column(verbose_name="CPF", accessor=tables.A('pessoa_fis_info.cpf'), orderable=True)
    cnpj = tables.Column(verbose_name="CNPJ", accessor=tables.A('pessoa_jur_info.cnpj'))
    id = tables.Column(verbose_name="Cód.", order_by='id')
    nome_razao_social = tables.Column(verbose_name="Nome / Razão Social", order_by='nome_razao_social')
    endereco_padrao = tables.Column(verbose_name="Endereço")
    site_padrao = tables.Column(verbose_name="Site", accessor=tables.A('site_padrao.site'))
    email_padrao = tables.Column(verbose_name="Email", accessor=tables.A('email_padrao.email'))
    telefone_padrao = tables.Column(verbose_name="Telefone", accessor=tables.A('telefone_padrao.telefone'))
    nascimento = tables.Column(verbose_name="Nascimento", accessor=tables.A('pessoa_fis_info.nascimento'))
    cep = tables.Column(verbose_name="CEP", accessor=tables.A('endereco_padrao.cep'))
    banco_padrao = tables.Column(verbose_name="Banco")
    data_criacao = tables.Column(verbose_name="Data de cadastro")
    data_edicao = tables.Column(verbose_name="Data de edição")
    proxima_visita = tables.Column(verbose_name="Próxima visita")
    inscricao_municipal = tables.Column(verbose_name="Inscrição Municipal")
    informacoes_adicionais = tables.Column(verbose_name="Informações adicionais")
    limite_de_credito = tables.Column(verbose_name="Limite de crédito")
    comissao_vendedor = tables.Column(verbose_name="Comissão do vendedor")
    inscricao_estadual = tables.Column(verbose_name="Inscrição Estadual", accessor=tables.A('pessoa_jur_info.inscricao_estadual'))
    sit_fiscal = tables.Column(verbose_name="Situação fiscal", accessor=tables.A('pessoa_jur_info.sit_fiscal'))

    class Meta:
        model = Cliente
        sequence = ('id', 'nome_razao_social', 'cpf', 'cnpj', 'inscricao_estadual', 'inscricao_municipal',
                    'endereco_padrao', 'cep', 'telefone_padrao',
                    'email_padrao', 'banco_padrao', 'nascimento', 'sit_fiscal')
        template_name = 'django_tables2/bootstrap.html'


class EntradasTable(ColumnShiftTable):

    id = tables.Column(verbose_name="Cód.")
    data_emissao = tables.Column(verbose_name="Emissão")
    data_vencimento = tables.Column(verbose_name="Vencimento")
    data_pagamento = tables.Column(verbose_name="Pagamento")
    descricao = tables.Column(verbose_name="Descrição")
    conta_corrente = tables.Column(verbose_name="Conta Corrente")
    depreciacao_bem = tables.Column(verbose_name="Bem de depreciação")
    depreciacao_anos = tables.Column(verbose_name="Depreciação (anos)")
    centro_custo = tables.Column(verbose_name="Centro de custo")
    grupo_plano = tables.Column(verbose_name="Grupo / Plano de contas")

    class Meta:
        model = Entrada
        template_name = 'django_tables2/bootstrap.html'
        sequence = ('id', 'data_emissao', 'data_vencimento', 'data_pagamento', 'status', 'descricao',
                    'centro_custo', 'grupo_plano')


class SaidasTable(ColumnShiftTable):
    id = tables.Column(verbose_name="Cód.")
    data_emissao = tables.Column(verbose_name="Emissão")
    data_vencimento = tables.Column(verbose_name="Vencimento")
    data_pagamento = tables.Column(verbose_name="Pagamento")
    descricao = tables.Column(verbose_name="Descrição")
    conta_corrente = tables.Column(verbose_name="Conta Corrente")
    depreciacao_bem = tables.Column(verbose_name="Bem de depreciação")
    depreciacao_anos = tables.Column(verbose_name="Depreciação (anos)")
    centro_custo = tables.Column(verbose_name="Centro de custo")
    grupo_plano = tables.Column(verbose_name="Grupo / Plano de contas")

    class Meta:
        model = Entrada
        template_name = 'django_tables2/bootstrap.html'
        sequence = ('id', 'data_emissao', 'data_vencimento', 'data_pagamento', 'status', 'descricao',
                    'centro_custo', 'grupo_plano')


class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return 'Total: ' + str(sum(bound_column.accessor.resolve(row) for row in table.data))


class SummingColumnMoeda(tables.Column):
    def render_footer(self, bound_column, table):
        return 'Total: R$ ' + str(sum(bound_column.accessor.resolve(row) for row in table.data))


class ProdutosTable(ColumnShiftTable):

    codigo = tables.Column(verbose_name="Código")
    codigo_barras = tables.Column(verbose_name="Código de barras")
    descricao = tables.Column(verbose_name="Descrição")
    genero = tables.Column(verbose_name="Gênero")
    producao = tables.Column(verbose_name="Produção")
    unidade = tables.Column(verbose_name="Unidade de medida")
    inf_adicionais = tables.Column(verbose_name="Informações adicionais")
    ncm = tables.Column(verbose_name="NCM")
    isbn = tables.Column(verbose_name="ISBN")
    cest = tables.Column(verbose_name="CEST")
    cfop_padrao = tables.Column(verbose_name="CFOP")
    estoque_minimo = tables.Column(verbose_name="Estoque mínimo")
    unidade_de_medida = tables.Column(verbose_name="Unidade de medida (volume)")
    custo_x_quantidade = tables.Column(
        verbose_name="Custo X Quantidade",
        accessor=tables.A('get_custo_x_quantidade',),
        footer=SummingColumnMoeda().footer
    )
    venda_x_quantidade = tables.Column(
        verbose_name="Venda X Quantidade",
        accessor=tables.A('get_venda_x_quantidade'),
        footer=SummingColumnMoeda().footer
    )
    estoque_atual = SummingColumn()

    class Meta:
        model = Produto
        template_name = 'django_tables2/bootstrap.html'


class VendasTable(ColumnShiftTable):

    class Meta:
        model = PedidoVenda
        template_name = 'django_tables2/bootstrap.html'


class Cliente2Table(tables.Table):
    class Meta:
        model = Cliente
