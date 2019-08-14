# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.crm2.models import Oportunidade


class OportunidadeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OportunidadeForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True

    class Meta:
        model = Oportunidade
        fields = ('empresa', 'cliente', 'categoria', 'responsavel', 'descricao', 'data_abertura',
                  'data_fechamento', 'probabilidade_fechamento', 'valor', 'contato', 'origem',
                  'nome_origem', 'situacao', 'data_sucesso',
                  'data_cancelamento', 'motivo_cancelamento', 'status_venda', 'etiquetas')

        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'responsavel':  forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'data_abertura': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'data_fechamento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'probabilidade_fechamento': forms.TextInput(attrs={'class': 'form-control percentual-mask'}),
            'valor': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'origem': forms.Select(attrs={'class': 'form-control'}),
            'nome_origem': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-control'}),
            'data_sucesso': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'data_cancelamento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'motivo_cancelamento': forms.Textarea(attrs={'class': 'form-control'}),
            'status_venda': forms.Select(attrs={'class': 'form-control'}),
            'etiquetas': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'empresa': _('Empresa'),
            'cliente': _('Cliente'),
            'categoria': _('Categoria'),
            'responsavel': _('Responsável'),
            'descricao': _('Descrição da oportunidade'),
            'data_abertura': _('Data de abertura'),
            'data_fechamento': _('Previsão de fechamento de negócio'),
            'probabilidade_fechamento': _('Probabilidade de fechamento (%)'),
            'valor': _('Valor do negócio (R$)'),
            'contato': _('Nome do contato'),
            'origem': _('Origem'),
            'nome_origem': _('Nome da origem'),
            'situacao': _('Situação'),
            'data_sucesso': _('Data de sucesso'),
            'data_cancelamento': _('Data de cancelamento'),
            'motivo_cancelamento': _('Motivo do cancelamento'),
            'status_venda': _('Status de Venda'),
            'etiquetas': 'Etiquetas',
        }



