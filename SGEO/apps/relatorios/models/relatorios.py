from django.db import models


class Relatorio(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.

        permissions = (
            ('acessar_relatorio_clientes', 'Acessar Clientes'),
            ('acessar_relatorio_entradas', 'Acessar Entradas'),
            ('acessar_relatorio_saidas', 'Acessar Saídas'),
            ('acessar_relatorio_produtos', 'Acessar Produtos'),
            ('acessar_relatorio_vendas', 'Acessar Vendas'),
            ('acessar_relatorio_dre', 'Acessar DRE'),
        )
