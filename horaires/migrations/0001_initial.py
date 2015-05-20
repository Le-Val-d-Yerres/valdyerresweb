# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('equipements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horaires',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name='Description')),
                ('lundi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('lundi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('lundi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('lundi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('lundi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('lundi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('lundi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('mardi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('mardi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('mardi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('mardi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('mardi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('mardi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('mardi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('mercredi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('mercredi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('mercredi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('mercredi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('mercredi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('mercredi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('mercredi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('jeudi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('jeudi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('jeudi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('jeudi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('jeudi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('jeudi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('jeudi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('vendredi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('vendredi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('vendredi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('vendredi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('vendredi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('vendredi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('vendredi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('samedi_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('samedi_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('samedi_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('samedi_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('samedi_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('samedi_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('samedi_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('dimanche_matin_debut', models.TimeField(null=True, verbose_name='Ouverture matin', blank=True)),
                ('dimanche_matin_fin', models.TimeField(null=True, verbose_name='Fermeture matin', blank=True)),
                ('dimanche_matin_ferme', models.BooleanField(default=False, verbose_name='Ferm\xe9 le matin')),
                ('dimanche_am_debut', models.TimeField(null=True, verbose_name='Ouverture apr\xe8s-midi', blank=True)),
                ('dimanche_am_fin', models.TimeField(null=True, verbose_name='Fermeture apr\xe8s-midi', blank=True)),
                ('dimanche_am_ferme', models.BooleanField(default=False, verbose_name="Ferm\xe9 l'apr\xe8s-midi")),
                ('dimanche_journee_continue', models.BooleanField(default=False, verbose_name='Journ\xe9e Continue')),
                ('equipement', models.ForeignKey(to='equipements.Equipement')),
            ],
            options={
                'ordering': ['equipement__ville__nom', 'equipement__nom'],
                'verbose_name_plural': 'Horaires',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=255, verbose_name='Nom de la p\xe9riode')),
                ('date_debut', models.DateField(default=datetime.date.today, verbose_name='D\xe9but de la p\xe9riode')),
                ('date_fin', models.DateField(default=datetime.date.today, verbose_name='Fin de la p\xe9riode')),
            ],
            options={
                'ordering': ['date_debut'],
                'verbose_name_plural': 'Periodes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='horaires',
            name='periodes',
            field=models.ManyToManyField(to='horaires.Periode'),
            preserve_default=True,
        ),
    ]
