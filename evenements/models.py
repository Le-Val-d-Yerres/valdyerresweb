# -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from localisations.models import Ville, Lieu

class Contact(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True)
    telephone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25, blank=True)
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)
    
    def __unicode__(self):
        return self.nom

class Saison(models.Model):
    nom = models.CharField(max_length=255)
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("date de fin")
    slug = models.SlugField(max_length=255, unique=True)
    
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
    
    def __unicode__(self):
        return self.nom

class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=200)
    description = models.TextField()
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("date de fin")
    contact = models.ForeignKey(Contact)
    image = FileBrowseField("Image", max_length=200, directory="evenements", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    url = models.URLField("Url (falcultatif)")
    cadre_evenement = models.ForeignKey(Saison)
    communal = models.BooleanField()
    communautaire = models.BooleanField()
    type = models.ForeignKey(TypeEvenement)
    lieu = models.ManyToManyField(Lieu)
    tarif = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def Lieu(self):
        return "\n;\n".join([s.nom_lieu for s in self.lieu.all()])

    def __unicode__(self):
        return self.nom
    