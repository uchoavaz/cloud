
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import CloudUser


class Droplet(models.Model):
    title = models.CharField(
        verbose_name=u"Título",
        max_length=50,
        unique=True)
    memory = models.IntegerField(verbose_name="Memória")
    processor = models.IntegerField(verbose_name="Core")

    class Meta:
        verbose_name = (u'Máquina Virtual')
        verbose_name_plural = (u'Máquinas Virtuais')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class UserDroplet(models.Model):
    user = models.ForeignKey(
        CloudUser,
        verbose_name=u"Usuário",
        related_name="user_droplet")
    droplet = models.ForeignKey(Droplet, related_name="user_droplet")
    name = models.CharField(
        verbose_name="Nome da VM", unique=True, max_length=15)
    ip = models.CharField(verbose_name="IP", unique=True, max_length=15)
    is_active = models.BooleanField(verbose_name="Ativo", default=False)

    class Meta:
        verbose_name = (u'Usuário máquina')
        verbose_name_plural = (u'Usuários máquinas')


class AvailableIps(models.Model):
    user = models.ForeignKey(
        CloudUser,
        verbose_name=u"Usuário",
        related_name="droplet_ip",
        null=True,
        blank=True)
    ip = models.CharField(verbose_name="IP", max_length=15)
    is_available = models.BooleanField(
        verbose_name="Disponivel ?", default=True)

    class Meta:
        verbose_name = (u'IP disponível')
        verbose_name_plural = (u"IP's disponíveis")
