# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-31 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0002_droplet_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdroplet',
            name='initial_password',
            field=models.CharField(blank=True, default='', max_length=5, unique=True, verbose_name='Senha inicial'),
        ),
    ]
