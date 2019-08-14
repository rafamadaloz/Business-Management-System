from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.integracao_financeira.models import PagSeguro


class PagSeguroForm(forms.ModelForm):
    class Meta:
        model = PagSeguro
        fields = ('email', 'token')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': _('E-mail'),
            'token': _('Token'),
        }
