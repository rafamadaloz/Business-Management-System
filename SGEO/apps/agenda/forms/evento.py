# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import inlineformset_factory

from SGEO.apps.agenda.models import Events


class EventsForm(forms.ModelForm):

    class Meta:
        model = Events
        fields = ('cor', 'event_name', 'start_date', 'end_date')
        widgets = {
            'cor': forms.Select(attrs={'class': 'form-control'}),
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control '}),
        }
        labels = {
            'cor': _('Cor do Evento'),
            'event_name': 'Descrição',
            'start_date': 'Início',
            'end_date': _('Fim'),
        }