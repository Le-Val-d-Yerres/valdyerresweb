# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Nom')),
                ('rue', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['ville__nom'],
                'verbose_name_plural': 'Lieux',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=150)),
                ('code_postal', models.CharField(max_length=10)),
                ('communaute_agglo', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('lien', models.URLField()),
                ('meta_description', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lieu',
            name='ville',
            field=models.ForeignKey(to='localisations.Ville'),
            preserve_default=True,
        ),
    ]
