# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.cadastro.models import Vendedor


class VendedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.fields['comissao_vendedor'].localize = True

    class Meta:
        model = Vendedor
        fields = ('nome_razao_social', 'tipo_pessoa', 'inscricao_municipal',
                  'informacoes_adicionais',
                  'comissao_vendedor', 'status_ativo', 'horas_trabalhadas_por_dia',
                  'dias_folga_por_semana')
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
            'comissao_vendedor': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'status_ativo': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'horas_trabalhadas_por_dia': forms.TextInput(attrs={'class': 'form-control'}),
            'dias_folga_por_semana': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('Razão Social'),
            'tipo_pessoa': _(''),
            'inscricao_municipal': _('Inscrição Municipal'),
            'informacoes_adicionais': _('Informações Adicionais'),
            'comissao_vendedor': 'Comissão do vendedor (%)',
            'proxima_visita': 'Data da próxima visita',
            'status_ativo': 'Ativo',
            'horas_trabalhadas_por_dia': 'Horas trabalhadas por dia',
            'dias_folga_por_semana': 'Dias de folga por semana'
        }

    def save(self, commit=True):
        instance = super(VendedorForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance
