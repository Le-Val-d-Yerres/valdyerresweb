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
            name='PageStatiqueService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=255, verbose_name=b'Titre')),
                ('slug', models.SlugField()),
                ('meta_description', models.CharField(max_length=200)),
                ('contenu', models.TextField()),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('index', models.IntegerField(verbose_name=b'Ordre apparition dans la liste')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name=b'Nom')),
                ('slug', models.SlugField()),
                ('index', models.IntegerField()),
                ('description', models.TextField(null=True, blank=True)),
                ('publie', models.BooleanField(default=False, verbose_name=b'Publi\xc3\xa9')),
                ('parent', models.ForeignKey(blank=True, to='services.Service', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pagestatiqueservice',
            name='service',
            field=models.ForeignKey(to='services.Service'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentattache',
            name='reference',
            field=models.ForeignKey(to='services.PageStatiqueService'),
            preserve_default=True,
        ),
    ]
