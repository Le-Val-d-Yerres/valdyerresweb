# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from services.models import Service
from django.db.models import permalink



class Annonce(models.Model):
    service = models.ForeignKey(Service,null=True)
    publie = models.BooleanField(verbose_name = "publication", default=False)
    intitule = models.CharField(max_length=255, verbose_name="Intitulé:")
    slug = models.SlugField()
    type_de_poste = models.CharField(max_length=255, verbose_name = "Type de Poste:",blank=True)
    secteur_activite = models.CharField(max_length=255, verbose_name = "Secteur d'activité:",blank=True)
    niveau_formation = models.TextField(verbose_name = "Niveau de formation requis:",blank=True)
    experience_requise = models.TextField(verbose_name = "Expérience requise:",blank=True)
    description_du_poste = models.TextField(verbose_name = "Description du poste:",blank=True)
    nom_employeur = models.TextField(verbose_name = "Nom de l'employeur:",blank=True)
    contact = models.TextField(verbose_name = "Contact:",blank=True)
    nb_postes = models.CharField(max_length=255, verbose_name="Nombre de postes:",blank=True)
    deplacement = models.TextField(verbose_name = "Déplacement:",blank=True)
    lieu_travail = models.TextField(verbose_name = "Lieu de travail:",blank=True)
    salaire_indicatif = models.CharField(max_length=255, verbose_name = "Salaire indicatif:",blank=True)
    
    def __unicode__(self):
        return self.intitule
    
    @permalink
    def get_absolute_url(self):
        return ('annonce-detail',(),{'annonce_slug':self.slug,'service_slug':self.service.slug})

# Classe d'interconnexion avec l'export XLS du logiciel
# utilisé par les maisons de l'emploi
class ImportGIDEM(models.Model):
    fichier_xls = models.FileField(upload_to="annoncesemploi/importsgidem/%Y/%m/%d")
    date_import = models.DateTimeField()
    
    
        
        