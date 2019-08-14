# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.plano.models import Plano


class PlanoForm(forms.ModelForm):

    class Meta:
        model = Plano
        fields = ('tipo_plano', 'tipo_pagamento', 'usuarios_adicionais', 'notas_adicionais',
                  'boletos_adicionais', 'status_ativo', 'cupom_desconto', 'codigo_parceiro')
        widgets = {
            'tipo_plano': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'usuarios_adicionais': forms.Select(attrs={'class': 'form-control'}),
            'notas_adicionais': forms.Select(attrs={'class': 'form-control'}),
            'boletos_adicionais': forms.Select(attrs={'class': 'form-control'}),
            # 'valor': forms.CharField(attrs={'class': 'form-control decimal-mask'}),
            'cupom_desconto': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_parceiro': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'tipo_plano': _('Plano'),
            'tipo_pagamento': _('Recorrência'),
            'usuarios_adicionais': 'Quantidade de usuários adicionais',
            'notas_adicionais': 'Quantidade de notas fiscais adicionais',
            'boletos_adicionais': 'Quantidade de boletos adicionais',
            'cupom_desconto': 'Cupom de Desconto',
            'codigo_parceiro': 'Código de Parceiro',
        }
