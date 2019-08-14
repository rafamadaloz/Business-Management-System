# -*- coding: utf-8 -*-

from django import forms
from decimal import Decimal

from SGEO.apps.cadastro.models.servico import Servico


class ServicoForm(forms.ModelForm):
    valor_custo = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='Valor de Custo',
                               required=False)
    valor_venda = forms.DecimalField(max_digits=16, decimal_places=2, localize=True, widget=forms.TextInput(
        attrs={'class': 'form-control decimal-mask', 'placeholder': 'R$ 0,00'}), initial=Decimal('0.00'), label='Valor de Venda',
                                     required=False)

    def __init__(self, *args, **kwargs):
        super(ServicoForm, self).__init__(*args, **kwargs)
        self.fields['valor_custo'].localize = True
        self.fields['valor_venda'].localize = True

    class Meta:
        model = Servico
        fields = ('codigo', 'descricao', 'tipo', 'categoria', 'valor_custo', 'valor_venda', 'inf_adicionais',
                  'nbs', 'codigo_municipal_servico', 'codigo_tributacao_municipal', 'status_ativo')
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'inf_adicionais': forms.TextInput(attrs={'class': 'form-control'}),
            'nbs': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_municipal_servico': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_tributacao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'status_ativo': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'codigo': 'Código',
            'descricao': 'Descrição',
            'categoria': 'Categoria',
            'tipo': 'Tipo de Serviço',
            'inf_adicionais': 'Informações Adicionais',
            'nbs': 'NBS',
            'codigo_tributacao_municipal': 'Código tributário municipal',
            'codigo_municipal_servico': 'Código municipal de serviço',
            'status_ativo': 'Ativo',
        }
