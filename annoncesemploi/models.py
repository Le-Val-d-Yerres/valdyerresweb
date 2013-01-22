# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from services.models import Service



class Annonce(models.Model):
    service = models.ForeignKey(Service,null=True)
    publie = models.BooleanField(verbose_name = "publication")
    intitule = models.CharField(max_length=255, verbose_name="Intitulé:")
    slug = models.SlugField()
    type_de_poste = models.CharField(max_length=255, verbose_name = "Type de Poste:")
    secteur_activite = models.CharField(max_length=255, verbose_name = "Secteur d'activité:")
    niveau_formation = models.TextField(verbose_name = "Niveau de formation requis:")
    experience_requise = models.TextField(verbose_name = "Expérience requise:")
    description_du_poste = models.TextField(verbose_name = "Description du poste:")
    nom_employeur = models.TextField(verbose_name = "Nom de l'employeur:")
    contact = models.TextField(verbose_name = "Contact:")
    nb_postes = models.CharField(max_length=255, verbose_name="Nombre de postes:")
    deplacement = models.TextField(verbose_name = "Déplacement:")
    lieu_travail = models.TextField(verbose_name = "Lieu de travail:")
    salaire_indicatif = models.CharField(max_length=255, verbose_name = "Salaire indicatif:")
    
    def __unicode__(self):
        return self.intitule
    

# Classe d'interconnexion avec l'export XLS du logiciel
# utilisé par les maisons de l'emploi
class ImportGIDEM(models.Model):
    fichier_xls = models.FileField(upload_to="annoncesemploi/importsgidem/%Y/%m/%d")
    date_import = models.DateTimeField()
    
    
        
        