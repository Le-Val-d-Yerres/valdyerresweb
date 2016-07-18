# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0002_auto_20150528_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('sexe', models.CharField(default=b'ind', max_length=5, choices=[(b'ind', 'Indetermin\xe9'), (b'homme', 'Homme'), (b'femme', 'femme')])),
                ('photo', models.ImageField(upload_to=b'affgen', null=True, verbose_name=b'Photo', blank=True)),
                ('publie', models.BooleanField(default=False, verbose_name='Publi\xe9')),
                ('ville', models.ForeignKey(to='localisations.Ville')),
            ],
            options={
                'ordering': ['nom'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MandatAgglo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('index', models.PositiveSmallIntegerField(verbose_name=b"ordre d'apparition")),
                ('elu', models.ForeignKey(to='affgen.Elu')),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': "Mandat dans l'agglo",
                'verbose_name_plural': "Mandats dans l'agglo",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QualifMandat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('feminin', models.CharField(max_length=255)),
                ('index', models.PositiveSmallIntegerField(verbose_name=b"ordre d'apparition")),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TitreHorsAgglo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('index', models.PositiveSmallIntegerField(verbose_name=b"ordre d'apparition")),
                ('elu', models.ForeignKey(to='affgen.Elu')),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mandatagglo',
            name='qualif',
            field=models.ForeignKey(to='affgen.QualifMandat'),
            preserve_default=True,
        ),
    ]
