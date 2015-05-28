# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('evenements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvenementCrd',
            fields=[
            ],
            options={
                'verbose_name': '\xc9v\xe9nement Conservatoire',
                'proxy': True,
                'verbose_name_plural': '\xc9v\xe9nements Conservatoires',
            },
            bases=('evenements.evenement',),
        ),
        migrations.AlterModelOptions(
            name='typeevenement',
            options={'ordering': ['nom']},
        ),
        migrations.AddField(
            model_name='evenement',
            name='categorie',
            field=models.CharField(default=b'aut', max_length=3, choices=[(b'bib', 'Biblioth\xe8ques/M\xe9diat\xe8ques'), (b'crd', 'Conservatoires'), (b'sty', 'Sothevy'), (b'aut', 'Autres')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evenement',
            name='public',
            field=models.CharField(default=b'pub', max_length=3, choices=[(b'adt', 'Adulte'), (b'enf', 'Enfant'), (b'pub', 'Tout public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evenement',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Image (facultatif)', blank=True),
            preserve_default=True,
        ),
    ]
