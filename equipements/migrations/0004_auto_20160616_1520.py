# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipements', '0003_tarifspecifique'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tarifspecifique',
            options={'ordering': ['categorie__index', 'index'], 'verbose_name_plural': 'Tarifs Sp\xe9cifiques'},
        ),
    ]
