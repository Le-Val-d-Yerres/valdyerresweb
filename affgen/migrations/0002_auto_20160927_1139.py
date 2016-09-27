# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('affgen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cptrendu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name=b'Date du conseil')),
                ('entite', models.CharField(default=b'vyvs', max_length=5, choices=[(b'vyvs', 'Val d\u2019Yerres Val de Seine'), (b'casvs', 'Val de Seine'), (b'cavt', 'Val d\u2019Yerres')])),
                ('document', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Document PDF')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': "Mandat dans l'agglo",
                'verbose_name_plural': "Mandats dans l'agglo",
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='elu',
            name='sexe',
            field=models.CharField(default=b'ind', max_length=5, choices=[(b'ind', 'Indetermin\xe9'), (b'homme', 'Homme'), (b'femme', 'Femme')]),
            preserve_default=True,
        ),
    ]
