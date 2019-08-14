# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'agenda'
urlpatterns = [
    url(r'calendario/$',
        views.AgendaView.as_view(), name='agendaview'),
]