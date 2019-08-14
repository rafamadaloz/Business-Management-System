# -*- coding: utf-8 -*-

from django.db import models

COR_ESCOLHAR = [
    ('#FFD700', 'Amarelo'),
    ('#0071c5', 'Azul Turquesa'),
    ('#FF4500', 'Laranja'),
    ('#8B4513', 'Marrom'),
    ('#1C1C1C', 'Preto'),
    ('#436EEE', 'Royal Blue'),
    ('#A020F0', 'Roxo'),
    ('#40E0D0', 'Turquesa'),
    ('#228B22', 'Verde'),
    ('#8B0000', 'Vermelho')
]


class Etiqueta(models.Model):
    cor = models.CharField(max_length=7)
    descricao = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Etiqueta"
        permissions = (
            ("view_etiqueta", "Can view etiqueta"),
        )

    def __str__(self):
        return self.descricao