# -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from localisations.models import Lieu
from django.core.urlresolvers import reverse
from django.db.models import permalink

class EquipementFonction(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Fonction")
    pluriel = models.CharField(max_length=255, verbose_name="Nom de la fonction au pluriel")
    picto = FileBrowseField("Pictogramme", max_length=200, directory="picto/equipements", extensions=[".png"])
    slug = models.SlugField(max_length=255,unique=True)

    def __unicode__(self):
        return self.nom
    
class Equipement(Lieu):
    fonction = models.ForeignKey(EquipementFonction)
    email = models.EmailField("Mail (facultatif)", max_length=254, blank=True)
    telephone = models.CharField(max_length=25)
    fax = models.CharField("Fax (facultatif)", max_length=25, blank=True, null=True)
    presentation = models.TextField(blank=True)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image (facultatif)", max_length=200, directory="equipements", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    
    def __unicode__(self):
        return self.nom
    
    @permalink
    def get_absolute_url(self):
        return ('equipement-details',(),{'equipement_slug':self.slug,'fonction_slug':self.fonction.slug})
    
class Facilite(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    importance = models.IntegerField("Degrée d'Importance (de 0 à 100)")
    picto = FileBrowseField("Pictogramme", max_length=200, directory="picto", extensions=[".png"])
    slug = models.SlugField(max_length=255,unique=True)
    
    def __unicode__(self):
        return self.nom
    
class Facilites(models.Model):
    equipement = models.ForeignKey(Equipement)
    facilites = models.ManyToManyField(Facilite)
    
    def __unicode__(self):
        return self.equipement.nom_lieu
    
    def Equipement(self):
        return self.equipement.nom_lieu
    
    def Facilites(self):
        i = 1
        for s in self.facilites.all():
            if i == 1:
                resultat = s.nom+" - "+str(s.importance)
                i=i+1
            else:
                resultat = resultat+" ; "+s.nom+" - "+str(s.importance)
            return resultat

    class Meta:
        verbose_name_plural = u"Facilités => Equipement"