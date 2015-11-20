# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evenements', '0003_auto_20151012_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='public',
            field=models.CharField(default=b'pub', max_length=3, choices=[(b'adt', 'Adulte'), (b'enf', 'Enfant'), (b'pub', 'Tout public'), (b'ent', 'Entreprises')]),
            preserve_default=True,
        ),
    ]
