# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localisations', '0001_initial'),
        ('equipements', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentAttache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Nom')),
                ('document', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('meta_description', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('debut', models.DateTimeField(verbose_name=b'Date de d\xc3\xa9but')),
                ('fin', models.DateTimeField(verbose_name=b'Date de fin')),
                ('image', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Image', blank=True)),
                ('url', models.URLField(null=True, verbose_name=b"Un lien vers plus d'infos: (facultatif)", blank=True)),
                ('url_reservation', models.URLField(null=True, verbose_name=b"Un lien vers la page de reservation: (facultatif, annule le lien vers plus d'infos) ", blank=True)),
                ('publish', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('page_accueil', models.BooleanField(default=False, verbose_name=b"Page d'accueil")),
                ('complet', models.BooleanField(default=False, verbose_name=b'Ce spectacle est complet')),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['-debut'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisateur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('meta_description', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('logo', filebrowser.fields.FileBrowseField(max_length=255, null=True, verbose_name=b'Image', blank=True)),
                ('url', models.URLField(verbose_name=b'Site de cet organisateur:  (facultatif) ', blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name=b'Mail (facultatif)', blank=True)),
                ('telephone', models.CharField(max_length=25)),
                ('fax', models.CharField(max_length=25, verbose_name=b'Fax (facultatif)', blank=True)),
                ('rue', models.CharField(max_length=255)),
                ('orga_equipement', models.ForeignKey(blank=True, to='equipements.Equipement', null=True)),
                ('orga_service', models.ForeignKey(blank=True, to='services.Service', null=True)),
                ('orga_ville', models.ForeignKey(related_name='orga_orga_ville', blank=True, to='localisations.Ville', null=True)),
                ('ville', models.ForeignKey(to='localisations.Ville')),
            ],
            options={
                'ordering': ['ville__nom'],
                'verbose_name_plural': 'Organisateurs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intitule', models.CharField(max_length=255, verbose_name=b'Intitul\xc3\xa9 ')),
                ('prix', models.FloatField(default=None, null=True, verbose_name=b'Prix (s\xc3\xa9parateur point ex : 0.5 )')),
                ('evenement', models.ForeignKey(to='evenements.Evenement')),
            ],
            options={
                'verbose_name_plural': 'Prix',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Saison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('debut', models.DateTimeField(verbose_name=b'Date de d\xc3\xa9but')),
                ('fin', models.DateTimeField(verbose_name=b'date de fin')),
                ('description', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Festival',
            fields=[
                ('saison_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='evenements.Saison')),
            ],
            options={
            },
            bases=('evenements.saison',),
        ),
        migrations.CreateModel(
            name='SaisonCulturelle',
            fields=[
                ('saison_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='evenements.Saison')),
            ],
            options={
            },
            bases=('evenements.saison',),
        ),
        migrations.CreateModel(
            name='TypeEvenement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='festival',
            name='saison_culture',
            field=models.ForeignKey(to='evenements.SaisonCulturelle'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evenement',
            name='cadre_evenement',
            field=models.ForeignKey(to='evenements.Saison'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evenement',
            name='lieu',
            field=models.ForeignKey(to='localisations.Lieu'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evenement',
            name='organisateur',
            field=models.ManyToManyField(to='evenements.Organisateur'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='evenement',
            name='type',
            field=models.ForeignKey(to='evenements.TypeEvenement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentattache',
            name='reference',
            field=models.ForeignKey(to='evenements.Evenement'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EvenementBib',
            fields=[
            ],
            options={
                'verbose_name': '\xc9v\xe9nement Biblioth\xe8que',
                'proxy': True,
                'verbose_name_plural': '\xc9v\xe9nements Biblioth\xe8ques',
            },
            bases=('evenements.evenement',),
        ),
    ]
