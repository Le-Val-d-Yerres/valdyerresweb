# -*- coding: utf-8 -*-
from django.db import models
from equipements.models import Equipement
import datetime

# Create your models here.

class Periode(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Nom de la période")
    date_debut = models.DateField(u"Début de la période", default=datetime.date.today)
    date_fin = models.DateField(u"Fin de la période", default=datetime.date.today)
    
    class Meta:
        verbose_name_plural = "Periodes"

class Horaires(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Description")
    equipement = models.ForeignKey(Equipement)
    periodes = models.ManyToManyField(Periode)
    
    lundi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    lundi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    lundi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    lundi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    lundi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    lundi_am_ferme = models.BooleanField(u"Fermé l'après-midi",blank=True)
    lundi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    mardi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    mardi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    mardi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    mardi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    mardi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    mardi_am_ferme = models.BooleanField(u"Fermé l'après-midi",blank=True)
    mardi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    
    mercredi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    mercredi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    mercredi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    mercredi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    mercredi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    mercredi_am_ferme = models.BooleanField(u"Fermé l'après-midi",blank=True)
    mercredi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    jeudi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    jeudi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    jeudi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    jeudi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    jeudi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    jeudi_am_ferme = models.BooleanField(u"Fermé l'après-midi",blank=True)
    jeudi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    vendredi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    vendredi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    vendredi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    vendredi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    vendredi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    vendredi_am_ferme = models.BooleanField(u"Fermé l'après-midi",blank=True)
    vendredi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    samedi_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    samedi_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    samedi_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    samedi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    samedi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    samedi_am_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    samedi_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    dimanche_matin_debut = models.TimeField(u"Ouverture matin",blank=True)
    dimanche_matin_fin = models.TimeField(u"Fermeture matin",blank=True)
    dimanche_matin_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    dimanche_am_debut = models.TimeField(u"Ouverture après-midi",blank=True)
    dimanche_am_fin = models.TimeField(u"Fermeture après-midi",blank=True)
    dimanche_am_ferme = models.BooleanField(u"Fermé le matin",blank=True)
    dimanche_journee_continue = models.BooleanField(u"Journée Continue",blank=True)
    
    class Meta:
        verbose_name_plural = "Horaires"

    