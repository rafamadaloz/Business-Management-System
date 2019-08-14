# -*- coding: utf-8 -*-

from django.db import models

class Frase(models.Model):
    frase = models.CharField(max_length=500)
    autor = models.CharField(max_length=255)