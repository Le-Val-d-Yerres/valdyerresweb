# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipement',
            name='type',
            field=models.CharField(default=b'aut', max_length=3, choices=[(b'bib', 'Biblioth\xe8ques/M\xe9diat\xe8ques'), (b'crd', 'Conservatoires'), (b'aut', 'Autres')]),
            preserve_default=True,
        ),
    ]
