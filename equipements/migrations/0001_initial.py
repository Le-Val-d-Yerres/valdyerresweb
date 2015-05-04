# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerte',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Titre')),
                ('texte_lien', models.CharField(max_length=255)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Alertes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlertesReponses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('rue', models.CharField(max_length=255)),
                ('codePostal', models.CharField(max_length=10)),
                ('ville', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=75)),
                ('message', models.TextField()),
                ('ip', models.IPAddressField()),
                ('date', models.DateTimeField()),
                ('etat', models.BooleanField(default=False)),
                ('alerte', models.ForeignKey(to='equipements.Alerte')),
            ],
            options={
                'ordering': ['etat', '-date'],
                'verbose_name_plural': 'Alertes Reponses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipement',
            fields=[
                ('lieu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='localisations.Lieu')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Mail (facultatif)', blank=True)),
                ('telephone', models.CharField(max_length=25, blank=True)),
                ('fax', models.CharField(max_length=25, null=True, verbose_name=b'Fax (facultatif)', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b'Site web', blank=True)),
                ('presentation', models.TextField(blank=True)),
                ('meta_description', models.CharField(max_length=200)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Image (facultatif)', blank=True)),
                ('alerte', models.ForeignKey(default=None, blank=True, to='equipements.Alerte', null=True)),
            ],
            options={
                'ordering': ('fonction__nom', 'ville__nom'),
            },
            bases=('localisations.lieu',),
        ),
        migrations.CreateModel(
            name='EquipementFonction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Fonction')),
                ('pluriel', models.CharField(max_length=255, verbose_name=b'Nom de la fonction au pluriel')),
                ('logo', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Logo', blank=True)),
                ('picto', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Pictogramme pour geolocalisation')),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('service', models.ForeignKey(verbose_name=b'Service Gestionnaire', blank=True, to='services.Service', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facilite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('importance', models.IntegerField(verbose_name=b"Degr\xc3\xa9e d'importance (de 0 + important \xc3\xa0 100 - important ). Entre 0 et 20 c'est g\xc3\xa9olocalisable au del\xc3\xa0 de 20 non.")),
                ('picto', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Pictogramme')),
                ('picto_geoloc', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b'Pictogramme pour la g\xc3\xa9olocalisation', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ('importance',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Facilites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equipement', models.ForeignKey(to='localisations.Lieu')),
                ('facilites', models.ManyToManyField(to='equipements.Facilite')),
            ],
            options={
                'verbose_name_plural': 'Facilit\xe9s => Equipement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(max_length=255, verbose_name=b'D\xc3\xa9signation : (ex: "Entr\xc3\xa9e Adulte ")')),
                ('info_additionelle', models.CharField(max_length=255, null=True, verbose_name=b'Infos additionelles : (facultatif)', blank=True)),
                ('index', models.IntegerField(verbose_name=b"Ordre d'apparition (0 = en haut de liste)")),
                ('prix_residents', models.FloatField(verbose_name=b'Tarif r\xc3\xa9sidents ( 0 = gratuit  )')),
                ('prix_non_residents', models.FloatField(verbose_name=b'Tarif non r\xc3\xa9sidents ( 0 = gratuit  )')),
            ],
            options={
                'ordering': ['categorie__index', 'index'],
                'verbose_name_plural': 'Tarifs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TarifCategorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Cat\xc3\xa9gorie de tarif')),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('index', models.IntegerField(verbose_name=b"Ordre d'apparition (0 = le plus important et tarif de base affich\xc3\xa9 pour l'\xc3\xa9quipement)")),
                ('equipement_fonction', models.ForeignKey(verbose_name=b"Cat\xc3\xa9gorie d'\xc3\xa9quipement concern\xc3\xa9e", to='equipements.EquipementFonction')),
            ],
            options={
                'ordering': ['index', 'equipement_fonction__nom'],
                'verbose_name_plural': 'Cat\xe9gorie des tarifs',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tarif',
            name='categorie',
            field=models.ForeignKey(to='equipements.TarifCategorie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipement',
            name='fonction',
            field=models.ForeignKey(to='equipements.EquipementFonction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alertesreponses',
            name='equipement',
            field=models.ForeignKey(to='equipements.Equipement'),
            preserve_default=True,
        ),
    ]
