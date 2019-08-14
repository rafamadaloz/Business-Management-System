# -*- coding: utf-8 -*-

from django.db import models

UF_SIGLA = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('EX', 'EX'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
]

class CadastroCompraCertificadoA1(models.Model):
    nome_socio = models.CharField(max_length=255)
    cpf = models.CharField(max_length=32)
    rg = models.CharField(max_length=32)
    orgao_emissor = models.CharField(max_length=32)
    email = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=32)
    uf = models.CharField(max_length=3, choices=UF_SIGLA)
    profissao = models.CharField(max_length=32)
