# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
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
            name='Magazine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre')),
                ('slug', models.SlugField(max_length=255)),
                ('date_parution', models.DateField()),
                ('document', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Document PDF')),
                ('image', models.ImageField(upload_to=b'magazines/img', blank=True)),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre')),
                ('slug', models.SlugField(max_length=255)),
                ('meta_description', models.CharField(max_length=200)),
                ('image', filebrowser.fields.FileBrowseField(max_length=200, null=True, verbose_name=b"Image principale de l'article (facultatif)", blank=True)),
                ('contenu', models.TextField()),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('date_mise_a_jour', models.DateTimeField()),
                ('carroussel', models.BooleanField(default=False, verbose_name=b"Pr\xc3\xa9sence dans le carroussel de la page d'accueil")),
                ('index_carroussel', models.IntegerField(default=0, verbose_name=b"Ordre d'affichage dans le caroussel (0 = premier)")),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actualite',
            fields=[
                ('pagebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='editorial.PageBase')),
                ('date_publication', models.DateTimeField()),
                ('page_accueil', models.BooleanField(default=False, verbose_name=b"Affichage en page d'accueil ?")),
            ],
            options={
            },
            bases=('editorial.pagebase',),
        ),
        migrations.CreateModel(
            name='PageStatique',
            fields=[
                ('pagebase_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='editorial.PageBase')),
                ('date_creation', models.DateTimeField()),
                ('note_page_accueil', models.BooleanField(default=False, verbose_name=b"Lister dans les notes de la page d'accueil")),
            ],
            options={
            },
            bases=('editorial.pagebase',),
        ),
        migrations.CreateModel(
            name='RapportActivite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre', blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('date_parution', models.DateField()),
                ('document', filebrowser.fields.FileBrowseField(max_length=200, verbose_name=b'Document PDF')),
                ('image', models.ImageField(upload_to=b'rapports/img')),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='documentattache',
            name='reference',
            field=models.ForeignKey(to='editorial.PageBase'),
            preserve_default=True,
        ),
    ]
