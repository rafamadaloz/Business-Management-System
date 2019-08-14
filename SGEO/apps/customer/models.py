from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from datetime import datetime

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default='admin')
    password = models.CharField(max_length=30, default='admin')
    email = models.CharField(max_length=100, unique=True, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=30, unique=True, null=True, blank=True)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass