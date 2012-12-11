# -*- coding: utf-8 -*-

from django.db import models
from localisations.models import Lieu

class Cinema(Lieu):
    id_allocine_cine = models.CharField(max_length=255, verbose_name="Identifiant Allociné")
    image = models.ImageField(upload_to="cinemas",verbose_name="Photo du lieu",blank=True, null=True)
    meta_description = models.CharField(max_length=255, verbose_name="Méta description")
    email = models.EmailField(blank=True, null=True,verbose_name="Email")
    telephone = models.CharField(max_length=25,blank=True, null=True, verbose_name="Téléphone")
    fax = models.CharField(max_length=25, blank=True, null=True)
    url = models.URLField(blank=True, null=True, verbose_name="Site web")
    hash_maj = models.CharField(max_length=42)
    
    def __unicode__(self):
        return self.nom
    
class Film(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre film")
    id_allocine_film = models.CharField(max_length=255, verbose_name="Identifiant Allociné du Film")
    duree = models.IntegerField(verbose_name="Durée du film")
    url_allocine_image = models.URLField(verbose_name="URL affiche du film sur allociné")
    image = models.ImageField(upload_to="cinema", verbose_name="Affiche du film")
    
    def __unicode__(self):
        return self.titre
    
class Seance(models.Model):
    film = models.ForeignKey(Film)
    cinema = models.ForeignKey(Cinema)
    id_allocine_film = models.CharField(max_length=255, verbose_name="Identifiant Allociné du Film")
    date_debut = models.DateTimeField(verbose_name="Date et heure de début du film")
    date_fin = models.DateTimeField(verbose_name="Date et heure de fin du film")
    format = models.CharField(max_length=255, verbose_name="Format ( facultatif )", blank=True, null=True)
    version_lang = models.CharField(max_length=255, verbose_name="Langue")
    version_vo = models.BooleanField(verbose_name="Version originale")