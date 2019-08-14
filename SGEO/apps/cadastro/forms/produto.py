# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.cadastro.models import Produto, Unidade, Marca, Categoria, Fornecedor, StatusVenda
from SGEO.apps.estoque.models import LocalEstoque

from decimal import Decimal


class ProdutoForm(forms.ModelForm):
    custo = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='Custo', required=False)
    venda = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='Venda', required=False)

    # Estoque
    estoque_inicial = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask'}), label='Qtd. em estoque inicial', initial=Decimal('0.00'), required=False)
    fornecedor = forms.ChoiceField(choices=[(None, '----------')], widget=forms.Select(
        attrs={'class': 'form-control'}), label='Fornecedor', required=False)
    local_dest = forms.ModelChoiceField(queryset=LocalEstoque.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}), empty_label=None, label='Localização do estoque de destino', required=False)

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['estoque_minimo'].localize = True
        self.fields['peso_liquido'].localize = True
        self.fields['peso_bruto'].localize = True
        self.fields['peso_com_embalagem'].localize = True
        self.fields['depreciacao'].localize = True
        self.fields['altura'].localize = True
        self.fields['altura_com_embalagem'].localize = True
        self.fields['largura_com_embalagem'].localize = True
        self.fields['largura'].localize = True
        self.fields['profundidade'].localize = True
        self.fields['profundidade_com_embalagem'].localize = True
        self.fields['fornecedor'].choices = list(self.fields['fornecedor'].choices) + [(
            fornecedor.id, fornecedor) for fornecedor in Fornecedor.objects.all()]

    class Meta:
        model = Produto
        fields = ('codigo', 'codigo_barras', 'descricao', 'categoria', 'marca', 'unidade', 'ncm', 'venda', 'custo', 'inf_adicionais',
                  'origem', 'cest', 'cfop_padrao', 'grupo_fiscal', 'estoque_minimo', 'controlar_estoque', 'modelo',
                  'genero', 'isbn', 'eangtin', 'status_ativo', 'producao', 'depreciacao', 'peso_liquido',
                  'peso_bruto', 'volumes', 'itens_por_caixa', 'altura', 'largura', 'profundidade', 'unidade_de_medida',
                  'peso_com_embalagem', 'altura_com_embalagem', 'largura_com_embalagem', 'profundidade_com_embalagem',
                  'validade', 'controlado_por_lote')
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-control'}),
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'inf_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
            'origem': forms.Select(attrs={'class': 'form-control'}),
            'cest': forms.TextInput(attrs={'class': 'form-control'}),
            'cfop_padrao': forms.Select(attrs={'class': 'form-control'}),
            'grupo_fiscal': forms.Select(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'controlar_estoque': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'eangtin': forms.TextInput(attrs={'class': 'form-control'}),
            'status_ativo': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'producao': forms.Select(attrs={'class': 'form-control'}),
            'depreciacao': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'peso_liquido': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'peso_bruto': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'volumes': forms.TextInput(attrs={'class': 'form-control'}),
            'itens_por_caixa': forms.TextInput(attrs={'class': 'form-control'}),
            'altura': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'largura': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'profundidade': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'unidade_de_medida': forms.Select(attrs={'class': 'form-control'}),
            'peso_com_embalagem': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'altura_com_embalagem': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'largura_com_embalagem': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'profundidade_com_embalagem': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'validade': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'controlado_por_lote': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'codigo': _('Código'),
            'codigo_barras': _('Código de Barras (GTIN/EAN)'),
            'descricao': _('Descrição'),
            'categoria': _('Categoria'),
            'marca': _('Marca'),
            'unidade': _('Unidade'),
            'ncm': _('NCM'),
            'inf_adicionais': _('Informações adicionais'),
            'origem': _('Origem'),
            'cest': _('CEST'),
            'cfop_padrao': _('CFOP (Padrão)'),
            'grupo_fiscal': _('Grupo Fiscal (Padrão)'),
            'estoque_minimo': _('Qtd. em estoque mínima'),
            'controlar_estoque': _('Controlar estoque deste produto?'),
            'modelo': _('Modelo'),
            'genero': 'Gênero',
            'isbn': 'ISBN',
            'eangtin': 'EAN/GTIN',
            'status_ativo': 'Ativo',
            'producao': 'Produção',
            'depreciacao': 'Depreciação R$',
            'peso_liquido': 'Peso Líquido (Kg)',
            'peso_bruto': 'Peso Bruto (Kg)',
            'volumes': 'Volumes',
            'itens_por_caixa': 'Itens por caixa',
            'altura': 'Altura',
            'largura': 'Largura',
            'profundidade': 'Profundidade',
            'unidade_de_medida': 'Unidade de medida',
            'peso_com_embalagem': 'Peso com embalagem (Kg)',
            'altura_com_embalagem': 'Altura com embalagem',
            'largura_com_embalagem': 'Largura com embalagem',
            'profundidade_com_embalagem': 'Profundidade com embalagem',
            'validade': 'Data de validade',
            'controlado_por_lote': 'Controlado por lote'
        }

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ('categoria_desc',)
        widgets = {
            'categoria_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'categoria_desc': _('Categoria'),
        }


class MarcaForm(forms.ModelForm):

    class Meta:
        model = Marca
        fields = ('marca_desc',)
        widgets = {
            'marca_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'marca_desc': _('Marca'),
        }


class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = ('sigla_unidade', 'unidade_desc',)
        widgets = {
            'unidade_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla_unidade': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'unidade_desc': _('Nome descritivo'),
            'sigla_unidade': _('Sigla'),
        }

class StatusVendaForm(forms.ModelForm):

    class Meta:
        model = StatusVenda
        fields = ('status_venda', 'posicao_navegacao')
        widget = {
            'status_venda': forms.TextInput(attrs={'class': 'form-control'}),
            'posicao_navegacao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'status_venda': _('Descrição'),
            'posicao_navegacao': _('Posição da coluna na navegação'),
        }
