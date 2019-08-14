# -*- coding: utf-8 -*-

from django.db import models

BANCOS = [
    ('001', '001 - BANCO DO BRASIL S.A.'),
    ('004', '004 - BANCO DO NORDESTE DO BRASIL S.A.'),
    ('021', '021 - BANESTES S.A. BANCO DO ESTADO DO ESPIRITO SANTO'),
    ('033', '033 - BANCO SANTANDER (BRASIL) S.A.'),
    ('041', '041 - BANCO DO ESTADO DO RIO GRANDE DO SUL S.A.'),
    ('104', '104 - CAIXA ECONOMICA FEDERAL'),
    ('237', '237 - BANCO BRADESCO S.A.'),
    ('341', '341 - BANCO ITAÚ S.A.'),
    ('399', '399 - HSBC BANK BRASIL S.A. - BANCO MULTIPLO'),
    ('422', '422 - BANCO SAFRA S.A.'),
    ('748', '748 - BANCO COOPERATIVO SICREDI S.A.'),
    ('756', '756 - BANCO COOPERATIVO DO BRASIL S.A. - BANCOOB'),
    ('757', '757 - BANCO KEB DO BRASIL S.A.'),
]

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


class ConfiguracaoBoleto(models.Model):
    nome_razao_social = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=32)
    cep = models.CharField(max_length=9)
    estado = models.CharField(max_length=3, choices=UF_SIGLA)
    cidade = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=80, null=True, blank=True)
    instrucoes = models.CharField(
        max_length=500, null=True, blank=True)
    carteira = models.CharField(max_length=6)
    banco = models.CharField(
        max_length=3, choices=BANCOS)
    agencia = models.CharField(max_length=8)
    conta = models.CharField(max_length=32)
    digito = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Configuração de Boleto"
        permissions = (
            ("view_configuracaoboleto", "Can view configuracaoboleto"),
        )
