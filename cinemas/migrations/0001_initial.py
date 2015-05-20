# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='localisations.Lieu')),
                ('id_allocine_cine', models.CharField(max_length=255, verbose_name=b'Identifiant Allocin\xc3\xa9')),
                ('image', models.ImageField(upload_to=b'cinemas', null=True, verbose_name=b'Photo du lieu', blank=True)),
                ('meta_description', models.CharField(max_length=255, verbose_name=b'M\xc3\xa9ta description')),
                ('email', models.EmailField(max_length=75, null=True, verbose_name=b'Email', blank=True)),
                ('telephone', models.CharField(max_length=25, null=True, verbose_name=b'T\xc3\xa9l\xc3\xa9phone', blank=True)),
                ('fax', models.CharField(max_length=25, null=True, blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'Site web', blank=True)),
                ('hash_maj', models.CharField(max_length=42)),
            ],
            options={
            },
            bases=('localisations.lieu',),
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre film')),
                ('id_allocine_film', models.CharField(max_length=255, verbose_name=b'Identifiant Allocin\xc3\xa9 du Film')),
                ('duree', models.IntegerField(verbose_name=b'Dur\xc3\xa9e du film')),
                ('url_allocine_image', models.URLField(verbose_name=b'URL affiche du film sur allocin\xc3\xa9')),
                ('image', models.ImageField(upload_to=b'cinema', null=True, verbose_name=b'Affiche du film', blank=True)),
                ('note', models.FloatField(default=0, verbose_name=b'Note des utilisateurs allocin\xc3\xa9')),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_allocine_film', models.CharField(max_length=255, verbose_name=b'Identifiant Allocin\xc3\xa9 du Film')),
                ('date_debut', models.DateTimeField(verbose_name=b'Date et heure de d\xc3\xa9but du film')),
                ('date_fin', models.DateTimeField(verbose_name=b'Date et heure de fin du film')),
                ('format', models.CharField(max_length=255, null=True, verbose_name=b'Format ( facultatif )', blank=True)),
                ('version_lang', models.CharField(max_length=255, verbose_name=b'Langue')),
                ('version_vo', models.BooleanField(default=False, verbose_name=b'Version originale')),
                ('cinema', models.ForeignKey(to='cinemas.Cinema')),
                ('film', models.ForeignKey(to='cinemas.Film')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
