# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-12-15 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FicheInscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=None, editable=False, max_length=36, null=True)),
                ('dateinscription', models.DateTimeField(auto_now=True)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('datenaissance', models.DateField()),
                ('sexe', models.CharField(choices=[('H', 'Homme'), ('F', 'Femme')], default='F', max_length=1)),
                ('email', models.EmailField(max_length=254)),
                ('adresse', models.CharField(max_length=255)),
                ('code_postal', models.CharField(max_length=255)),
                ('ville', models.CharField(max_length=255)),
                ('profession', models.CharField(max_length=255)),
                ('telephone', models.CharField(max_length=255)),
                ('adultereferent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='epn.FicheInscription')),
            ],
        ),
    ]
