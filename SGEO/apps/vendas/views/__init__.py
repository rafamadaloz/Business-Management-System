# -*- coding: utf-8 -*-

from .vendas import (AdicionarOrcamentoVendaView, AdicionarPedidoVendaView, OrcamentoVendaListView,
                     OrcamentoVendaVencidosListView, OrcamentoVendaVencimentoHojeListView, PedidoVendaListView,
                     PedidoVendaAtrasadosListView, PedidoVendaEntregaHojeListView, EditarOrcamentoVendaView,
                     EditarPedidoVendaView, GerarPedidoVendaView, CancelarOrcamentoVendaView,
                     CancelarPedidoVendaView, GerarCopiaOrcamentoVendaView, GerarCopiaPedidoVendaView,
                     GerarPDFOrcamentoVenda, GerarPDFPedidoVenda)
from .vendas_pdv import VendasPdvListView
from .pagamento import *
from .ajax_views import InfoVenda
