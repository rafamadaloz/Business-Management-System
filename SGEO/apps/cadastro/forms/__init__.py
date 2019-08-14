# -*- coding: utf-8 -*-

from .pessoa_forms import PessoaJuridicaForm, PessoaFisicaForm
from .inline_formsets import EnderecoFormSet, TelefoneFormSet, EmailFormSet, SiteFormSet, BancoFormSet, DocumentoFormSet, LoteFormSet

from .empresa import EmpresaForm, MinhaEmpresaForm
from .cliente import ClienteForm, GrupoForm
from .fornecedor import FornecedorForm
from .transportadora import TransportadoraForm, VeiculoFormSet
from .vendedor import VendedorForm
from .servico import ServicoForm

from .produto import ProdutoForm, CategoriaForm, UnidadeForm, MarcaForm, StatusVendaForm
