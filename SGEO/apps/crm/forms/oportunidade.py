# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Oportunidade
from django.forms import inlineformset_factory

class OportunidadeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OportunidadeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Oportunidade

        fields = ('empresa', 'cliente', 'categoria')

        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'empresa': _('Empresa'),
            'cliente': _('Cliente'),
            'categoria': _('Categoria'),
        }

    def save(self, commit=True):
        instance = super(OportunidadeForm, self).save(commit=False)
        instance.criado_por = self.request.user
        if commit:
            instance.save()
        return instance

