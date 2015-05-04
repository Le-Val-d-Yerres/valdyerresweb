# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publie', models.BooleanField(default=False, verbose_name=b'publication')),
                ('intitule', models.CharField(max_length=255, verbose_name=b'Intitul\xc3\xa9:')),
                ('slug', models.SlugField()),
                ('type_de_poste', models.CharField(max_length=255, verbose_name=b'Type de Poste:', blank=True)),
                ('secteur_activite', models.CharField(max_length=255, verbose_name=b"Secteur d'activit\xc3\xa9:", blank=True)),
                ('niveau_formation', models.TextField(verbose_name=b'Niveau de formation requis:', blank=True)),
                ('experience_requise', models.TextField(verbose_name=b'Exp\xc3\xa9rience requise:', blank=True)),
                ('description_du_poste', models.TextField(verbose_name=b'Description du poste:', blank=True)),
                ('nom_employeur', models.TextField(verbose_name=b"Nom de l'employeur:", blank=True)),
                ('contact', models.TextField(verbose_name=b'Contact:', blank=True)),
                ('nb_postes', models.CharField(max_length=255, verbose_name=b'Nombre de postes:', blank=True)),
                ('deplacement', models.TextField(verbose_name=b'D\xc3\xa9placement:', blank=True)),
                ('lieu_travail', models.TextField(verbose_name=b'Lieu de travail:', blank=True)),
                ('salaire_indicatif', models.CharField(max_length=255, verbose_name=b'Salaire indicatif:', blank=True)),
                ('service', models.ForeignKey(to='services.Service', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportGIDEM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fichier_xls', models.FileField(upload_to=b'annoncesemploi/importsgidem/%Y/%m/%d')),
                ('date_import', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
