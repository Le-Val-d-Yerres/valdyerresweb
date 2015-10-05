# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disciplinestagecrd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('index', models.IntegerField()),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'discipline stage',
                'verbose_name_plural': 'disciplines stage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fichestagecrd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('commentaires', models.TextField(null=True)),
                ('choix_1', models.ForeignKey(related_name='choix_1', to='forms.Disciplinestagecrd', null=True)),
                ('choix_2', models.ForeignKey(related_name='choix_2', to='forms.Disciplinestagecrd', null=True)),
                ('choix_3', models.ForeignKey(related_name='choix_3', to='forms.Disciplinestagecrd', null=True)),
            ],
            options={
                'ordering': ['nom'],
                'verbose_name': 'fiche stage',
                'verbose_name_plural': 'fiches stage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Intitulestage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255)),
                ('duree', models.CharField(max_length=255)),
                ('index', models.IntegerField()),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'intitul\xe9 stage',
                'verbose_name_plural': 'intitul\xe9s stage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('toussaint_1', models.BooleanField(default=False)),
                ('toussaint_2', models.BooleanField(default=False)),
                ('hiver_1', models.BooleanField(default=False)),
                ('hiver_2', models.BooleanField(default=False)),
                ('paques_1', models.BooleanField(default=False)),
                ('paques_2', models.BooleanField(default=False)),
                ('ete_1', models.BooleanField(default=False)),
                ('ete_2', models.BooleanField(default=False)),
                ('fiche', models.ForeignKey(to='forms.Fichestagecrd')),
                ('intitule', models.ForeignKey(to='forms.Intitulestage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
