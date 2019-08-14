# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'pdv'
urlpatterns = [
    url(r'pdv/$', views.PDVView.as_view(), name='pdvview'),
    url(r'sale/$', views.SaleView.as_view(), name='sale'),
    url(r'autocomplete/$', views.AutoCompleteView.as_view(), name='search-products'),
    url(r'add-to-cart/$', views.AddToCart.as_view(), name='add-to-cart'),
    url(r'clear-cart/$', views.ClearCart.as_view(), name='clear-cart'),
    url(r'checkout/$', views.CheckOut.as_view(), name='checkout'),
    path('delete-from-cart/<int:produto_id>/', views.DeleterCartProduct.as_view(), name='delete-from-cart'),
]
