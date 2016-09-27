# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0002_auto_20150528_1442'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ville',
            options={'ordering': ['nom'], 'verbose_name_plural': 'Lieux'},
        ),
    ]
