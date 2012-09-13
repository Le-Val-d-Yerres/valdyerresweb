# -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from localisations.models import Ville, Lieu
from model_utils.managers import InheritanceManager

class Organisateur(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    meta_description = models.CharField(max_length=200)
    description = models.TextField()
    logo = FileBrowseField("Image", max_length=255, directory="evenements", extensions=[".jpg", ".png", ".gif", ".jpeg"], blank=True, null=True)
    url = models.URLField("Site de cet organisateur:  (facultatif) ", blank=True)
    email = models.EmailField("Mail (facultatif)", max_length=255, blank=True)
    telephone = models.CharField(max_length=25)
    fax = models.CharField("Fax (facultatif)", max_length=25, blank=True)
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)
    
    def __unicode__(self):
        return self.nom

class Saison(models.Model):
    nom = models.CharField(max_length=255)
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("date de fin")
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    
    objects = InheritanceManager()
    
    def __unicode__(self):
        return self.nom

class SaisonCulturelle(Saison):
    def __unicode__(self):
        return self.nom
    
class Festival(Saison):
    saison_culture = models.ForeignKey(SaisonCulturelle)
    
    def __unicode__(self):
        return self.nom

class TypeEvenement(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    def __unicode__(self):
        return self.nom

class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=200)
    description = models.TextField()
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("date de fin (facultatif)")
    organisateur = models.ManyToManyField(Organisateur)
    image = FileBrowseField("Image", max_length=255, directory="evenements", extensions=[".jpg", ".png", ".gif", ".jpeg"], blank=True, null=True)
    url = models.URLField("Eventuellement un lien: ", blank=True)
    cadre_evenement = models.ForeignKey(Saison)
    type = models.ForeignKey(TypeEvenement)
    lieu = models.ForeignKey(Lieu)
    publish = models.BooleanField("Publié")
    haut_page = models.BooleanField("Haut de page")
    slug = models.SlugField(max_length=255, unique=True)
    
    def Organisateurs(self):
        return "\n;\n".join([s.nom for s in self.organisateur.all()])
        
    def __unicode__(self):
        return self.nom
    
    def monthyeardebut(self):
        return self.debut.strftime("%m")+"-"+self.debut.strftime("%Y")
        
    
class Prix (models.Model):
    gratuit = models.BooleanField()
    nom = models.CharField(max_length=255)
    prix = models.FloatField("Prix (facultatif)", blank=True)
    
    def __unicode__(self):
        if self.gratuit:
            resultat = self.nom+" - Gratuit"
        else:
            resultat = self.nom+" - "+str(self.prix)+u"€"
        return resultat
    
    class Meta:
        verbose_name_plural = "Prix"
    
class Tarification(models.Model):
    evenement = models.ForeignKey(Evenement)
    prix = models.ManyToManyField(Prix)
    
    def __unicode__(self):
        return self.evenement.nom
    
    def Evenement(self):
        return self.evenement.nom
    
    def Prix(self):
        i = 1
        for s in self.prix.all():
            if s.gratuit:
                if i == 1:
                    resultat = s.nom+" - Gratuit"
                    i=i+1
                else:
                    resultat = resultat+" ; "+s.nom+" - Gratuit"
            else:
                if i == 1:
                    resultat = s.nom+" - "+str(s.prix)+u"€"
                    i=i+1
                else:
                    resultat = resultat+" ; "+s.nom+" - "+str(s.prix)+u"€"
        return resultat
    
    
    

    
    
    
    
    
    
    
    
    
    
    