# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-11 03:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vm', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userdroplet',
            unique_together=set([]),
        ),
    ]