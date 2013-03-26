# -*- coding: utf-8 -*-
from django.db import models
from services.models import Service
from filebrowser.fields import FileBrowseField
from localisations.models import Lieu
from django.core.urlresolvers import reverse
from django.db.models import permalink
from model_utils.managers import InheritanceManager


class EquipementFonction(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Fonction")
    pluriel = models.CharField(max_length=255, verbose_name="Nom de la fonction au pluriel")
    logo = FileBrowseField("Logo", max_length=200, directory="picto/equipements", extensions=[".png"] ,blank=True, null=True)
    picto = FileBrowseField("Pictogramme pour geolocalisation", max_length=200, directory="picto/equipements", extensions=[".png"])
    slug = models.SlugField(max_length=255,unique=True)
    service = models.ForeignKey(Service,blank=True,null=True,verbose_name="Service Gestionnaire")

    def __unicode__(self):
        return self.nom
    
class Equipement(Lieu):
    fonction = models.ForeignKey(EquipementFonction)
    email = models.EmailField("Mail (facultatif)", max_length=254, blank=True)
    telephone = models.CharField(max_length=25,blank=True)
    fax = models.CharField("Fax (facultatif)", max_length=25, blank=True, null=True)
    url = models.URLField(blank=True, null=True, verbose_name="Site web")
    presentation = models.TextField(blank=True)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image (facultatif)", max_length=200, directory="equipements", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    
    def __unicode__(self):
        return self.ville.nom+" - "+ self.nom
    
    class Meta:
        ordering = ('fonction__nom','ville__nom',)
    
    @permalink
    def get_absolute_url(self):
        return ('equipement-details',(),{'equipement_slug':self.slug,'fonction_slug':self.fonction.slug})
    
class Facilite(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    importance = models.IntegerField("Degrée d'importance (de 0 + important à 100 - important ). Entre 0 et 20 c'est géolocalisable au delà de 20 non.")
    picto = FileBrowseField("Pictogramme", max_length=200, directory="picto", extensions=[".png"])
    picto_geoloc = FileBrowseField("Pictogramme pour la géolocalisation", max_length=200, directory="picto", extensions=[".png"], blank=True, null=True)
    slug = models.SlugField(max_length=255,unique=True)
    
    def __unicode__(self):
        return self.nom
    class Meta:
        ordering = ('importance',)
    
class Facilites(models.Model):
    equipement = models.ForeignKey(Lieu)
    facilites = models.ManyToManyField(Facilite)
    

    def __unicode__(self):
        return self.equipement.nom
    
    def Equipement(self):
        return self.equipement.nom
    
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
        
class TarifCategorie(models.Model):
    nom = models.CharField(max_length=255,verbose_name="Catégorie de tarif")
    slug = models.SlugField(max_length=255,unique=True)
    index = models.IntegerField("Ordre d'apparition (0 = le plus important et tarif de base affiché pour l'équipement)")
    equipement_fonction = models.ForeignKey(EquipementFonction, verbose_name="Catégorie d'équipement concernée")
    
    def __unicode__(self):
        return self.nom
    
    class Meta:
        verbose_name_plural = "Catégorie des tarifs"
        ordering = ['index','equipement_fonction__nom']
        
class Tarif(models.Model):
    designation = models.CharField(max_length=255,verbose_name="Désignation : (ex: \"Entrée Adulte \")")
    info_additionelle = models.CharField(max_length=255,verbose_name="Infos additionelles : (facultatif)", blank = True , null = True)
    index = models.IntegerField("Ordre d'apparition (0 = en haut de liste)")
    categorie = models.ForeignKey(TarifCategorie)
    prix_residents = models.FloatField("Tarif résidents ( 0 = gratuit  )")
    prix_non_residents = models.FloatField("Tarif non résidents ( 0 = gratuit  )")
    
    def __unicode__(self):
        return self.designation
    
    class Meta:
        verbose_name_plural = "Tarifs"
        ordering = ['categorie__index','index']

        
    