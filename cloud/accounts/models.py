
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models

class CloudUserManager(BaseUserManager):
    def create_user(self,
                    username,
                    email,
                    password=None):
        user = self.model(
            email=email, username=username)
        user.set_password(password)
        user.is_active = True
        return user

    def create_superuser(self, username, email,
                         password):
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save()
        return user


class CloudUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="Nome do usuário", max_length=50, unique=True)
    email = models.EmailField(
        verbose_name=(u'E-mail'),
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True)

    is_staff = models.BooleanField(
        verbose_name=('Status de suporte'), default=False)

    is_active = models.BooleanField(
        verbose_name=(u'ativo'), default=True)
    full_name = models.CharField(
        verbose_name='Nome completo', max_length=100)

    short_name = models.CharField(
        verbose_name='Nome abreviado', max_length=50)

    created_at = models.DateTimeField(
        verbose_name=(u'data de inscrição'), default=timezone.now)

    updated_at = models.DateTimeField(
        verbose_name=(u'última atualização'),
        default=timezone.now)

    objects = CloudUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = (u'usuário')
        verbose_name_plural = (u'usuários')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.email
