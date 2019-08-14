# -*- coding: utf-8 -*-

from django import forms

from SGEO.apps.boletos.models import Boleto


class BoletoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoletoForm, self).__init__(*args, **kwargs)
        self.initial['status'] = '0'

    class Meta:
        model = Boleto
        fields = ('pagador', 'emissao', 'vencimento', 'documento',
                  'numero', 'titulo', 'valor', 'status', 'pedido_de_venda')
        widgets = {
            'pedido_de_venda': forms.Select(attrs={'class': 'form-control'}),
            'pagador': forms.Select(attrs={'class': 'form-control'}),
            'emissao': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'pagador': 'Cliente',
            'emissao': 'Emissao',
            'vencimento': 'Vencimento',
            'documento': 'Documento',
            'numero': 'Número',
            'titulo': 'Título',
            'valor': 'Valor',
            'status': 'Status',
            'pedido_de_venda': 'Pedido'
        }
