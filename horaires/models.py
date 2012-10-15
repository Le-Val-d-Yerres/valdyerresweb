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

class Jour():
    def __init__(self,heure_matin_debut =None,heure_matin_fin = None, heure_am_debut=None,heure_am_fin=None,matin_ferme=False,am_ferme=False,journee_continue=False,jourNom="",jourInt=42):
        self.heure_matin_debut = heure_matin_debut
        self.heure_matin_fin = heure_matin_fin
        self.heure_am_debut = heure_am_debut
        self.heure_am_fin = heure_am_fin
        self.matin_ferme = matin_ferme
        self.am_ferme = am_ferme
        self.journee_continue = journee_continue
        self.jourNom = jourNom
        self.jourInt = int(jourInt)

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
    
    def GetDay(self, day):
        monJour = Jour()
        monJour.jourInt = int(day)
        
        if day == 7:
            monJour.jourNom = "dimanche"
            monJour.heure_matin_debut = self.dimanche_matin_debut
            monJour.heure_matin_fin = self.dimanche_matin_fin
            monJour.heure_am_debut = self.dimanche_am_debut
            monJour.heure_am_fin = self.dimanche_am_fin
            monJour.matin_ferme = self.dimanche_matin_ferme
            monJour.am_ferme = self.dimanche_am_ferme
            monJour.journee_continue = self.dimanche_journee_continue
        
        if day == 1:
            monJour.jourNom = "lundi"
            monJour.heure_matin_debut = self.lundi_matin_debut
            monJour.heure_matin_fin = self.lundi_matin_fin
            monJour.heure_am_debut = self.lundi_am_debut
            monJour.heure_am_fin = self.lundi_am_fin
            monJour.matin_ferme = self.lundi_matin_ferme
            monJour.am_ferme = self.lundi_am_ferme
            monJour.journee_continue = self.lundi_journee_continue
        
        if day == 2:
            monJour.jourNom = "mardi"
            monJour.heure_matin_debut = self.mardi_matin_debut
            monJour.heure_matin_fin = self.mardi_matin_fin
            monJour.heure_am_debut = self.mardi_am_debut
            monJour.heure_am_fin = self.mardi_am_fin
            monJour.matin_ferme = self.mardi_matin_ferme
            monJour.am_ferme = self.mardi_am_ferme
            monJour.journee_continue = self.mardi_journee_continue
            
        if day == 3:
            monJour.jourNom = "mercredi"
            monJour.heure_matin_debut = self.mercredi_matin_debut
            monJour.heure_matin_fin = self.mercredi_matin_fin
            monJour.heure_am_debut = self.mercredi_am_debut
            monJour.heure_am_fin = self.mercredi_am_fin
            monJour.matin_ferme = self.mercredi_matin_ferme
            monJour.am_ferme = self.mercredi_am_ferme
            monJour.journee_continue = self.mercredi_journee_continue
            
        if day == 4:
            monJour.jourNom = "jeudi"
            monJour.heure_matin_debut = self.jeudi_matin_debut
            monJour.heure_matin_fin = self.jeudi_matin_fin
            monJour.heure_am_debut = self.jeudi_am_debut
            monJour.heure_am_fin = self.jeudi_am_fin
            monJour.matin_ferme = self.jeudi_matin_ferme
            monJour.am_ferme = self.jeudi_am_ferme
            monJour.journee_continue = self.jeudi_journee_continue
            
        if day == 5:
            monJour.jourNom = "vendredi"
            monJour.heure_matin_debut = self.vendredi_matin_debut
            monJour.heure_matin_fin = self.vendredi_matin_fin
            monJour.heure_am_debut = self.vendredi_am_debut
            monJour.heure_am_fin = self.vendredi_am_fin
            monJour.matin_ferme = self.vendredi_matin_ferme
            monJour.am_ferme = self.vendredi_am_ferme
            monJour.journee_continue = self.vendredi_journee_continue
        
        if day == 6:
            monJour.jourNom = "samedi"
            monJour.heure_matin_debut = self.samedi_matin_debut
            monJour.heure_matin_fin = self.samedi_matin_fin
            monJour.heure_am_debut = self.samedi_am_debut
            monJour.heure_am_fin = self.samedi_am_fin
            monJour.matin_ferme = self.samedi_matin_ferme
            monJour.am_ferme = self.samedi_am_ferme
            monJour.journee_continue = self.samedi_journee_continue
        
        return monJour
        
        
        
    