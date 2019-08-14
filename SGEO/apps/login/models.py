# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

NOTAS_ADICIONAL = (
    (u'0', u'0'),
    (u'1', u'1000'),
    (u'2', u'2000'),
)

USUARIOS_ADICIONAL = (
    (u'0', u'0'),
    (u'1', u'1'),
    (u'2', u'2'),
    (u'3', u'3'),
    (u'4', u'4'),
    (u'5', u'5'),
    (u'6', u'6'),
    (u'7', u'7'),
    (u'8', u'8'),
    (u'9', u'9'),
)

def user_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return 'imagens/usuarios/fotos_perfil/{0}_{1}{2}'.format(instance.user.username, instance.user.id, extension)


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_foto = models.ImageField(
        upload_to=user_directory_path, default='imagens/user.png', blank=True)
    user_capa_foto = models.ImageField(
        upload_to=user_directory_path, default='imagens/background-user.png', blank=True)

    def save(self, *args, **kwargs):
        # Deletar user_foto se ja existir uma
        try:
            obj = Usuario.objects.get(id=self.id)
            if obj.user_foto != self.user_foto and obj.user_foto != 'imagens/user.png':
                obj.user_foto.delete(save=False)
            if obj.user_capa_foto != self.user_capa_foto and obj.user_capa_foto != 'imagens/background-user.png':
                obj.user_capa_foto.delete(save=False)
        except:
            pass

        super(Usuario, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user

    def __str__(self):
        return u'%s' % self.user


@receiver(post_delete, sender=Usuario)
def foto_post_delete_handler(sender, instance, **kwargs):
    # Nao deletar a imagem default 'user.png'
    if instance.user_foto != 'imagens/user.png':
        instance.user_foto.delete(False)
    if instance.user_capa_foto != 'imagens/background-user.png':
        instance.user_capa_foto.delete(False)


class Plano(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(decimal_places=2, max_digits=13)
    qtd_notas = models.PositiveIntegerField()
    qtd_usuarios = models.PositiveIntegerField()


class UsuarioAdicionalPlano(models.Model):
    quantidade = models.PositiveIntegerField(primary_key=True)
    preco = models.DecimalField(decimal_places=2, max_digits=13)

    def __str__(self):
        return str(self.quantidade)


class NotaAdicionalPlano(models.Model):
    quantidade = models.PositiveIntegerField(primary_key=True)
    preco = models.DecimalField(decimal_places=2, max_digits=13)

    def __str__(self):
        return str(self.quantidade)


class ConfiguracoesDoPlano(models.Model):
    plano = models.ForeignKey('login.Plano', related_name='plano', on_delete=models.CASCADE)
    notas_adicional = models.ForeignKey('login.NotaAdicionalPlano', related_name='nota_adicional', on_delete=models.CASCADE)
    usuarios_adicional = models.ForeignKey('login.UsuarioAdicionalPlano', related_name='usuario_adicional', on_delete=models.CASCADE)
