# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-22 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('epn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ficheinscription',
            name='numero_adherent',
            field=models.CharField(blank=True, default=None, max_length=15, null=True),
        ),
    ]