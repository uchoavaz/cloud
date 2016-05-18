# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-18 20:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vm', '0002_auto_20160511_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailableIps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP')),
                ('is_available', models.BooleanField(default=True, verbose_name='Disponivel ?')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='droplet_ip', to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio')),
            ],
            options={
                'verbose_name': 'IP dispon\xedvel',
                'verbose_name_plural': "IP's dispon\xedveis",
            },
        ),
    ]