# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0002_auto_20150528_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActualiteDevEco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre')),
                ('slug', models.SlugField(max_length=255)),
                ('meta_description', models.CharField(max_length=200)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b"Image principale de l'article (facultatif)", blank=True)),
                ('contenu', models.TextField()),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('date_mise_a_jour', models.DateTimeField()),
                ('date_publication', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dirigeant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Photo du dirigeant', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('presentation', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentAttacheDevEco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Nom')),
                ('document', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Document')),
                ('reference', models.ForeignKey(to='deveco.ActualiteDevEco')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('meta_description', models.CharField(max_length=200)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b"Image / Logo de l'entreprise", blank=True)),
                ('presentation', models.TextField(null=True, blank=True)),
                ('rue', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('telephone', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('site_internet', models.URLField(null=True, blank=True)),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('ville', models.ForeignKey(to='localisations.Ville')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dirigeant',
            name='entreprise',
            field=models.ForeignKey(to='deveco.Entreprise'),
            preserve_default=True,
        ),
    ]
