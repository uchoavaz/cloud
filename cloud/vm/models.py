
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import CloudUser


STATUS_CHOICES = (
    (1, 'VM inativa'),
    (2, 'VM ativa'),
    (3, 'Criando VM'),
    (4, 'Editando VM')

)


class Droplet(models.Model):
    title = models.CharField(
        verbose_name=u"Título",
        max_length=50,
        unique=True)
    memory = models.IntegerField(verbose_name="Memória")
    processor = models.IntegerField(verbose_name="Core")
    disk = models.IntegerField(
        verbose_name="Tamanho do disco virtual (GB)", default=40)
    cost = models.FloatField(verbose_name="Custo ($)", default=5)

    class Meta:
        verbose_name = (u'Máquina Virtual')
        verbose_name_plural = (u'Máquinas Virtuais')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Image(models.Model):
    name = models.CharField(
        verbose_name="Nome", max_length=30, unique=True)
    name_path = models.CharField(
        verbose_name="Nome do caminho", max_length=255, unique=True)

    class Meta:
        verbose_name = (u'Imagem')
        verbose_name_plural = (u'Imagens')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class UserDroplet(models.Model):
    user = models.ForeignKey(
        CloudUser,
        verbose_name=u"Usuário",
        related_name="user_droplet")
    droplet = models.ForeignKey(
        Droplet,
        verbose_name=u"Droplet",
        related_name="user_droplet")
    image = models.ForeignKey(
        Image,
        verbose_name="Imagem",
        related_name="user_droplet")
    name = models.CharField(
        verbose_name="Nome da VM", unique=True, max_length=15)
    ip = models.CharField(verbose_name="IP", unique=True, max_length=15)
    status = models.IntegerField(
        verbose_name="Status", choices=STATUS_CHOICES, default=1)
    can_remove = models.BooleanField(
        verbose_name="Pode Excluir ?", default=False)
    initial_password = models.CharField(
        verbose_name="Senha inicial",
        unique=True, default="", blank=True, max_length=5)

    class Meta:
        verbose_name = (u'Usuário máquina')
        verbose_name_plural = (u'Usuários máquinas')


class AvailableIps(models.Model):
    ip = models.CharField(verbose_name="IP", max_length=15, unique=True)
    is_available = models.BooleanField(
        verbose_name="Disponivel ?", default=True)

    class Meta:
        verbose_name = (u'IP disponível')
        verbose_name_plural = (u"IP's disponíveis")
