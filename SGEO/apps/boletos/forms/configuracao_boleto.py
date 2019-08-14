# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from SGEO.apps.boletos.models import ConfiguracaoBoleto


class ConfiguracoesBoletoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoBoleto
        fields = ('carteira', 'banco', 'agencia', 'conta', 'digito', 'nome_razao_social', 'cpf_cnpj', 'cep',
                  'estado', 'cidade', 'bairro', 'logradouro',
                  'numero', 'complemento', 'instrucoes')
        labels = {
            'banco': _('Banco'),
            'agencia': _('Agência'),
            'conta': _('Conta'),
            'digito': _('Dígito'),
            'carteira': 'Carteira',
            'nome_razao_social': 'Nome / Razão Social',
            'cpf_cnpj': 'CPF/CNPJ',
            'cep': 'CEP',
            'estado': 'Estado',
            'cidade': 'Cidade',
            'bairro': 'Bairro',
            'logradouro': 'Logradouro',
            'numero': 'Número',
            'complemento': 'Complemento',
            'instrucoes': 'Instruções do boleto'
        }
        widgets = {
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control'}),
            'conta': forms.TextInput(attrs={'class': 'form-control'}),
            'digito': forms.TextInput(attrs={'class': 'form-control'}),
            'carteira': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
