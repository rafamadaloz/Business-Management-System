# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.crm2.models import Etiqueta

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = ('cor', 'descricao')
        widgets = {
            'cor': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cor': 'Cor',
            'descricao': 'Descrição',
        }