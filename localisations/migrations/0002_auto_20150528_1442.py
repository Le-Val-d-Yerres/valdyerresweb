# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lieu',
            options={'ordering': ['ville__nom', 'nom'], 'verbose_name_plural': 'Lieux'},
        ),
    ]
