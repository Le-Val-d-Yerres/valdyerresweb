# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from model_utils.managers import InheritanceManager
from django.db.models import permalink

# Create your models here.

class PageBase(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image principale de l'article (facultatif)", max_length=200, directory="editorial", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié")
    date_mise_a_jour = models.DateTimeField()
    carroussel = models.BooleanField("Présence dans le carroussel de la page d'accueil",default=False)
    index_carroussel = models.IntegerField("Ordre d'affichage dans le caroussel (0 = premier)",default=0)
    objects = InheritanceManager()
    
class PageStatique(PageBase):
    date_creation = models.DateTimeField()
    
    @permalink
    def get_absolute_url(self):
        return ('page-detail',(),{'page_slug':self.slug})
    
class Actualite(PageBase):
    
    date_publication = models.DateTimeField()
    page_accueil = models.BooleanField("Affichage en page d'accueil ?",default=False)
    
    @permalink
    def get_absolute_url(self):
        return ('actu-detail',(),{'actualite_slug':self.slug})
   
    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="editorial/docs", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageBase)
    
class Magazine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    date_parution = models.DateField()
    document = FileBrowseField("Document PDF", max_length=200, directory="magazines", extensions=[".pdf"])
    image = models.ImageField(upload_to="magazines",blank=True)
    publie = models.BooleanField(verbose_name="Publié")

     
class RapportActivite(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    date_parution = models.DateField()
    document = FileBrowseField("Document PDF", max_length=200, directory="rapports", extensions=[".pdf"])
    image = models.ImageField(upload_to="rapports") 
    publie = models.BooleanField(verbose_name="Publié")
