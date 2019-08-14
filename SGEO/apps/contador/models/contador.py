# -*- coding: utf-8 -*-

from django.db import models

class Contador(models.Model):
    conta_nfe = models.IntegerField(default=0)
    conta_nfce = models.IntegerField(default=0)

