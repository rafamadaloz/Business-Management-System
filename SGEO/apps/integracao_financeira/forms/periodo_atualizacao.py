from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.integracao_financeira.models import PeriodoIntegracao


class PeriodoIntegracaoForm(forms.ModelForm):
    class Meta:
        model = PeriodoIntegracao
        fields = ('data_inicio', 'data_fim')
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}, format='%d/%m/%Y %H:%M'),
            'data_fim': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker', 'autocomplete': 'off'}, format='%d/%m/%Y %H:%M'),
        }
        labels = {
            'data_inicio': _('De'),
            'data_fim': _('Até'),
        }

