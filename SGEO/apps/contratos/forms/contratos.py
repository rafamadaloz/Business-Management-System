# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.contratos.models import Contrato, TipoContrato


class ContratoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
        self.fields['valor_entrada'].localize = True
        self.fields['valor_periodo'].localize = True
        self.fields['valor_total'].localize = True
        self.fields['valor_comissao_vendedor_periodo'].localize = True
        self.fields['valor_comissao_vendedor_total'].localize = True


    class Meta:
        model = Contrato
        fields = ('empresa', 'cliente', 'tipo_contrato', 'condicao_pagamento',
                  'centro_custos', 'situacao', 'dia_vencimento', 'duracao_contrato', 'tipo_duracao_contrato',
                  'ultimo_reajuste', 'proximo_reajuste', 'data_termino', 'dias_carencia', 'valor_periodo',
                  'valor_total', 'numero_parcelas', 'intervalo', 'periodo', 'intervalo_dias',
                  'valor_entrada', 'vendedor', 'comissao_vendedor', 'valor_comissao_vendedor_periodo',
                  'valor_comissao_vendedor_total')

        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_contrato': forms.Select(attrs={'class': 'form-control'}),
            'condicao_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'centro_custos': forms.TextInput(attrs={'class': 'form-control'}),
            'situacao': forms.Select(attrs={'class': 'form-control'}),
            'dia_vencimento': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracao_contrato': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_duracao_contrato': forms.Select(attrs={'class': 'form-control'}),
            'ultimo_reajuste': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'proximo_reajuste': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'data_termino': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'dias_carencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_periodo': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'numero_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'intervalo': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'intervalo_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_entrada': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'vendedor': forms.Select(attrs={'class': 'form-control'}),
            'comissao_vendedor': forms.TextInput(attrs={'class': 'form-control decimal-mask-four'}),
            'valor_comissao_vendedor_periodo': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
            'valor_comissao_vendedor_total': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'readonly': True}),
        }

        labels = {
            'empresa': _('Empresa'),
            'cliente': _('Cliente'),
            'tipo_contrato': _('Tipo de contrato'),
            'condicao_pagamento': _('Condição de pagamento'),
            'centro_custos': _('Centro de custos'),
            'situacao': _('Situação'),
            'dia_vencimento': _('Dia de vencimento'),
            'duracao_contrato': _('Duração do contrato'),
            'tipo_duracao_contrato': _(''),
            'ultimo_reajuste': _('Último reajuste'),
            'proximo_reajuste': _('Próximo reajuste'),
            'data_termino': _('Data de término'),
            'dias_carencia': _('Dias de carência'),
            'valor_periodo': _('Valor por período'),
            'valor_total': _('Valor total'),
            'numero_parcelas': _('Número de parcelas'),
            'intervalo': _('Intervalo'),
            'periodo': _('Período'),
            'intervalo_dias': _('Dias de intervalo'),
            'valor_entrada': _('Valor de entrada'),
            'vendedor': _('Vendedor'),
            'comissao_vendedor': _('Comissão vendedor (%)'),
            'valor_comissao_vendedor_periodo': _('Valor comissão (período) R$'),
            'valor_comissao_vendedor_total': _('Valor comissão (total) R$'),
        }


class TipoContratoForm(forms.ModelForm):
    class Meta:
        model = TipoContrato
        fields = ('nome', 'template',)
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'template': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': _('Nome'),
            'template': _('Template'),
        }
