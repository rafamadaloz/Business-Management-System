# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

from SGEO.configs import DEBUG

app_name = 'base'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.BaseView.as_view(), name='base'),
]

if DEBUG:
    urlpatterns += [
        url(r'^404/$', views.handler404),
        url(r'^500/$', views.handler500),
    ]
