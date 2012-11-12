# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField

class Service(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.SlugField()
    index  = models.IntegerField()
    parent = models.ForeignKey('self', null= True,blank=True)
    description = models.TextField(null= True,blank=True)
    
    def __unicode__(self):
        return self.nom
    
    
class PageStatiqueService(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    meta_description = models.CharField(max_length=200)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié")
    index = models.IntegerField(verbose_name="Ordre apparition dans la liste")
    service = models.ForeignKey(Service)

    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageStatiqueService)