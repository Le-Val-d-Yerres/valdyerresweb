# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('evenements', '0005_auto_20160927_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentattache',
            name='document',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='documentattache',
            name='nom',
            field=models.CharField(max_length=255, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='categorie',
            field=models.CharField(choices=[('bib', 'Bibliothèques/Médiatèques'), ('crd', 'Conservatoires'), ('sty', 'Sothevy'), ('eco', 'Développement Économique'), ('aut', 'Autres')], default='aut', max_length=3),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='complet',
            field=models.BooleanField(default=False, verbose_name='Ce spectacle est complet'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='debut',
            field=models.DateTimeField(verbose_name='Date de début'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='fin',
            field=models.DateTimeField(verbose_name='Date de fin'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='image',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=255, null=True, verbose_name='Image (facultatif)'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='page_accueil',
            field=models.BooleanField(default=False, verbose_name="Page d'accueil"),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='public',
            field=models.CharField(choices=[('adt', 'Adulte'), ('enf', 'Enfant'), ('pub', 'Tout public'), ('ent', 'Entreprises')], default='pub', max_length=3),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='publish',
            field=models.BooleanField(default=False, verbose_name='Publié'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name="Un lien vers plus d'infos: (facultatif)"),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='url_reservation',
            field=models.URLField(blank=True, null=True, verbose_name="Un lien vers la page de reservation: (facultatif, annule le lien vers plus d'infos) "),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='Mail (facultatif)'),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='fax',
            field=models.CharField(blank=True, max_length=25, verbose_name='Fax (facultatif)'),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='logo',
            field=filebrowser.fields.FileBrowseField(blank=True, max_length=255, null=True, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='organisateur',
            name='url',
            field=models.URLField(blank=True, verbose_name='Site de cet organisateur:  (facultatif) '),
        ),
        migrations.AlterField(
            model_name='prix',
            name='intitule',
            field=models.CharField(max_length=255, verbose_name='Intitulé '),
        ),
        migrations.AlterField(
            model_name='prix',
            name='prix',
            field=models.FloatField(default=None, null=True, verbose_name='Prix (séparateur point ex : 0.5 )'),
        ),
        migrations.AlterField(
            model_name='saison',
            name='debut',
            field=models.DateTimeField(verbose_name='Date de début'),
        ),
        migrations.AlterField(
            model_name='saison',
            name='fin',
            field=models.DateTimeField(verbose_name='date de fin'),
        ),
    ]
