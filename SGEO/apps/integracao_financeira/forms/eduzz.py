from django import forms
from django.utils.translation import ugettext_lazy as _

from SGEO.apps.integracao_financeira.models import Eduzz


class EduzzForm(forms.ModelForm):
    class Meta:
        model = Eduzz
        fields = ('public_key', 'api_key')
        widgets = {
            'public_key': forms.TextInput(attrs={'class': 'form-control'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'public_key': _('Public Key'),
            'api_key': _('API Key'),
        }
