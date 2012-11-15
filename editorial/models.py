# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
# Create your models here.

class PageBase(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    meta_description = models.CharField(max_length=200)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié")
    date_mise_a_jour = models.DateTimeField()
    
class PageStatique(PageBase):
    date_creation = models.DateTimeField()
    


    
class Actualite(PageBase):
    logo = FileBrowseField("Logo de l'article (facultatif)", max_length=200, directory="editorial", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    date_publication = models.DateTimeField()
    page_accueil = models.BooleanField()
    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="editorial", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageStatique)
    
class Magazine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="magazines", extensions=[".pdf"])
    image = models.ImageField(upload_to="magazines",blank=True)
     
class RapportActivite(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="rapports", extensions=[".pdf"])
    image = models.ImageField(upload_to="rapports")