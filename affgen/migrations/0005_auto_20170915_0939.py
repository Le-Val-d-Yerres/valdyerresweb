# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-15 07:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('affgen', '0004_auto_20170912_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cptrendu',
            options={'ordering': ['date'], 'verbose_name': 'Compte rendu conseil', 'verbose_name_plural': 'Comptes rendus'},
        ),
    ]
