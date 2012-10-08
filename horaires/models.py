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
    
    def __unicode__(self):
        return self.nom
    
    def dateIn(self,date):
        if self.date_debut <= date and date <= self.date_fin:
            return True
        return False
    
    def periodIn (self,periode):
        if self.date_debut <= periode.date_debut and periode.date_fin <= self.date_fin:
            return True
        return False
    

class Horaires(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Description")
    equipement = models.ForeignKey(Equipement)
    periodes = models.ManyToManyField(Periode)
    
    lundi_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    lundi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    lundi_matin_ferme = models.BooleanField(u"Fermé le matin")
    lundi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    lundi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    lundi_am_ferme = models.BooleanField(u"Fermé l'après-midi")
    lundi_journee_continue = models.BooleanField(u"Journée Continue")
    
    mardi_matin_debut = models.TimeField(u"Ouverture matin",blank=True, null=True)
    mardi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    mardi_matin_ferme = models.BooleanField(u"Fermé le matin")
    mardi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    mardi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    mardi_am_ferme = models.BooleanField(u"Fermé l'après-midi")
    mardi_journee_continue = models.BooleanField(u"Journée Continue")
    
    
    mercredi_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    mercredi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    mercredi_matin_ferme = models.BooleanField(u"Fermé le matin")
    mercredi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    mercredi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    mercredi_am_ferme = models.BooleanField(u"Fermé l'après-midi")
    mercredi_journee_continue = models.BooleanField(u"Journée Continue")
    
    jeudi_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    jeudi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    jeudi_matin_ferme = models.BooleanField(u"Fermé le matin")
    jeudi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    jeudi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    jeudi_am_ferme = models.BooleanField(u"Fermé l'après-midi")
    jeudi_journee_continue = models.BooleanField(u"Journée Continue")
    
    vendredi_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    vendredi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    vendredi_matin_ferme = models.BooleanField(u"Fermé le matin")
    vendredi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    vendredi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    vendredi_am_ferme = models.BooleanField(u"Fermé l'après-midi")
    vendredi_journee_continue = models.BooleanField(u"Journée Continue")
    
    samedi_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    samedi_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    samedi_matin_ferme = models.BooleanField(u"Fermé le matin")
    samedi_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    samedi_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    samedi_am_ferme = models.BooleanField(u"Fermé le matin")
    samedi_journee_continue = models.BooleanField(u"Journée Continue")
    
    dimanche_matin_debut = models.TimeField(u"Ouverture matin",blank=True,null=True)
    dimanche_matin_fin = models.TimeField(u"Fermeture matin",blank=True,null=True)
    dimanche_matin_ferme = models.BooleanField(u"Fermé le matin")
    dimanche_am_debut = models.TimeField(u"Ouverture après-midi",blank=True,null=True)
    dimanche_am_fin = models.TimeField(u"Fermeture après-midi",blank=True,null=True)
    dimanche_am_ferme = models.BooleanField(u"Fermé le matin")
    dimanche_journee_continue = models.BooleanField(u"Journée Continue")
    
    class Meta:
        verbose_name_plural = "Horaires"
    
    def __unicode__(self):
        return self.nom
    def List_Periods(self):
        listPeriodes = self.periodes.all()
        txt = ""
        i=1
        for periode in listPeriodes:
            txt += periode.nom
            if i <  len(listPeriodes) :
                txt+=", "
            i=i+1
        return txt
    