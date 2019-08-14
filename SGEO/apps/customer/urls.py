from django.conf.urls import url
from . import views

app_name = 'customer'
urlpatterns = [

    url(r'^cadastro/$', views.ClientsList.as_view(), name='clientslist'),

]
