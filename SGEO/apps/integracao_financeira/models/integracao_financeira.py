from django.db import models

import locale
locale.setlocale(locale.LC_ALL, '')

PLATAFORMAS = [
    ('HM', 'Hotmart'),
    ('ED', 'Eduzz'),
    ('MP', 'Mercado Pago'),
    ('PS', 'PagSeguro'),
    ('CI', "Cielo")
]


class Hotmart(models.Model):
    key = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Integração Hotmart"
        permissions = (
            ("acessar_hotmart", "Acessar Hotmart"),
        )


class Eduzz(models.Model):
    public_key = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Integração Eduzz"
        permissions = (
            ("acessar_eduzz", "Acessar Eduzz"),
        )


class MercadoPago(models.Model):
    public_key = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Integração Mercado Pago"
        permissions = (
            ("acessar_mp", "Acessar Mercado Pago"),
        )


class PagSeguro(models.Model):
    email = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Integração Pagseguro"
        permissions = (
            ("acessar_ps", "Acessar Pagseguro"),
        )


class PeriodoIntegracao(models.Model):
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    plataforma = models.CharField(max_length=2, choices=PLATAFORMAS, null=True, blank=True)
