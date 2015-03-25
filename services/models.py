# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from django.db.models import permalink

class Service(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.SlugField()
    index  = models.IntegerField()
    parent = models.ForeignKey('self', null= True,blank=True)
    description = models.TextField(null= True,blank=True)
    publie = models.BooleanField(verbose_name="Publié", default=False)
    
    def __unicode__(self):
        return self.nom
    
    @permalink
    def get_absolute_url(self):
        return ('service-detail',(),{'service_slug':self.slug})
    
class PageStatiqueService(models.Model):
    service = models.ForeignKey(Service)
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    meta_description = models.CharField(max_length=200)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié", default=False)
    index = models.IntegerField(verbose_name="Ordre apparition dans la liste")
    
    def __unicode__(self):
        return self.titre
    

    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="services/docs", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageStatiqueService)