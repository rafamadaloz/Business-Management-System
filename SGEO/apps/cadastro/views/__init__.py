# -*- coding: utf-8 -*-

from .empresa import AdicionarEmpresaView, EmpresasListView, EditarEmpresaView
from .vendedor import AdicionarVendedorView, EditarVendedorView, VendedorListView
from .cliente import AdicionarClienteView, ClientesListView, EditarClienteView, ImportarClienteView
from .fornecedor import AdicionarFornecedorView, FornecedoresListView, EditarFornecedorView
from .transportadora import AdicionarTransportadoraView, TransportadorasListView, EditarTransportadoraView
from .produto import (AdicionarProdutoView, ProdutosListView, ProdutosBaixoEstoqueListView, EditarProdutoView,
                      AdicionarCategoriaView, CategoriasListView, EditarCategoriaView,
                      AdicionarUnidadeView, UnidadesListView, EditarUnidadeView,
                      AdicionarMarcaView, MarcasListView, EditarMarcaView, AdicionarStatusVendaView,
                      EditarStatusVendaView, StatusVendaListView, StatusVendaViewEmNavegacao,
                      AdicionarGrupoView, EditarGrupoView, GrupoListView)
from .servico import AdicionarServicoView, EditarServicoView, ServicosListView
from .ajax_views import InfoCliente, InfoFornecedor, InfoEmpresa, InfoTransportadora, InfoProduto
