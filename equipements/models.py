# -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from localisations.models import Lieu

class EquipementFonction(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Fonction")

    def __unicode__(self):
        return self.nom
    
class Equipement(Lieu):
    fonction = models.ForeignKey(EquipementFonction)
    email = models.EmailField(max_length=254, blank=True)
    telephone = models.CharField(max_length=25)
    fax = models.CharField(max_length=25, blank=True, null=True)
    presentation = models.TextField()
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image", max_length=200, directory="equipements", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    
    def __unicode__(self):
        return self.nom_lieu