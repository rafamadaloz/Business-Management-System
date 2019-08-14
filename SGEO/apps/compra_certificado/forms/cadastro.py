# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from SGEO.apps.compra_certificado.models import CadastroCompraCertificadoA1


class CadastroCompraCertificadoA1Form(forms.ModelForm):
    class Meta:
        model = CadastroCompraCertificadoA1
        fields = ('nome_socio', 'cpf', 'rg', 'orgao_emissor', 'email',
                  'data_nascimento', 'telefone', 'uf', 'profissao')
        widgets = {
            'nome_socio': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'orgao_emissor': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'SSP/RJ'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
            'profissao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_socio': _('Nome (Sócio Administrativo)'),
            'cpf': _('CPF'),
            'rg': _('RG'),
            'orgao_emissor': _('Órgão Emissor'),
            'email': _('Email'),
            'data_nascimento': _('Data de Nascimento'),
            'telefone': _('Telefone'),
            'uf': _('UF'),
            'profissao': _('Profissão')
        }

    def save(self, commit=True):
        instance = super(CadastroCompraCertificadoA1Form, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance