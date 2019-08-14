# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.cadastro.models import Cliente, Grupo


class ClienteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['limite_de_credito'].localize = True
        self.fields['limite_restante'].localize = True
        self.fields['comissao_vendedor'].localize = True

    class Meta:
        model = Cliente
        fields = ('nome_razao_social', 'tipo_pessoa', 'inscricao_municipal',
                  'limite_de_credito', 'indicador_ie', 'id_estrangeiro', 'informacoes_adicionais', 'grupo',
                  'limite_restante', 'comissao_vendedor', 'proxima_visita', 'status_ativo')
        widgets = {
            'nome_razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.RadioSelect(attrs={'class': 'form-control'}),
            'limite_de_credito': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'indicador_ie': forms.Select(attrs={'class': 'form-control'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control'}),
            'id_estrangeiro': forms.TextInput(attrs={'class': 'form-control'}),
            'informacoes_adicionais': forms.Textarea(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'limite_restante': forms.TextInput(attrs={'class': 'form-control decimal-mask', 'disabled': 'True'}),
            'comissao_vendedor': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'proxima_visita': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'status_ativo': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_razao_social': _('Razão Social'),
            'tipo_pessoa': _(''),
            'limite_de_credito': _('Limite de Crédito'),
            'indicador_ie': _('Indicador da IE do Destinatário'),
            'inscricao_municipal': _('Inscrição Municipal'),
            'id_estrangeiro': _('Documento legal (Estrangeiro)'),
            'informacoes_adicionais': _('Informações Adicionais'),
            'grupo': _('Grupo'),
            'limite_restante': 'Limite de crédito restante',
            'comissao_vendedor': 'Comissão do vendedor (%)',
            'proxima_visita': 'Data da próxima visita',
            'status_ativo': 'Ativo',
        }

    def save(self, commit=True):
        instance = super(ClienteForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance


class GrupoForm(forms.ModelForm):

    class Meta:
        model = Grupo
        fields = ('grupo_desc',)
        widgets = {
            'grupo_desc': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'grupo_desc': _('Grupo'),
        }
