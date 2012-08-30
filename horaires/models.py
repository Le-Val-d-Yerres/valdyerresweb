# -*- coding: utf-8 -*-
from django.db import models
from equipements.models import Equipement


# Create your models here.

class Horaires(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Nom de la période")
    equipement = models.ForeignKey(Equipement)
    date_debut = models.DateField(u"Début de la période")
    date_fin = models.DateField(u"Fin de la période")
    lundi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    lundi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    lundi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    lundi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    lundi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    mardi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    mardi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    mardi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    mardi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    mardi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    mercredi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    mercredi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    mercredi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    mercredi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    mercredi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    jeudi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    jeudi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    jeudi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    jeudi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    jeudi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    vendredi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    vendredi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    vendredi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    vendredi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    vendredi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    samedi_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    samedi_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    samedi_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    samedi_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    samedi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    dimanche_matin_debut = models.TimeField(u"Ouverture Matin",blank=True)
    dimanche_matin_fin = models.TimeField(u"Fermeture Matin",blank=True)
    dimanche_am_debut = models.TimeField(u"Ouverture Après-Midi",blank=True)
    dimanche_am_fin = models.TimeField(u"Fermeture Après-Midi",blank=True)
    dimanche_journee_continue = models.BooleanField(u"Journée Continue",blank=True)

class Vacances(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Nom de la période")
    date_debut = models.DateField(u"Début de la période")
    date_fin = models.DateField(u"Fin de la période")
    
class HorairesVacances(Horaires):
    vacances = models.ManyToManyField(Vacances)
    