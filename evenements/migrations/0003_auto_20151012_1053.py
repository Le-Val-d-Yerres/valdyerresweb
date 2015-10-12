# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evenements', '0002_auto_20150528_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvenementDevEco',
            fields=[
            ],
            options={
                'verbose_name': '\xc9v\xe9nement Dev Eco',
                'proxy': True,
                'verbose_name_plural': '\xc9v\xe9nements Dev Eco',
            },
            bases=('evenements.evenement',),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='categorie',
            field=models.CharField(default=b'aut', max_length=3, choices=[(b'bib', 'Biblioth\xe8ques/M\xe9diat\xe8ques'), (b'crd', 'Conservatoires'), (b'sty', 'Sothevy'), (b'eco', 'D\xe9veloppement \xc9conomique'), (b'aut', 'Autres')]),
            preserve_default=True,
        ),
    ]
