# -*- coding: utf-8 -*-

from django.db import models
from localisations.models import Ville
from filebrowser.fields import FileBrowseField


class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image / Logo de l'entreprise", max_length=200, directory="deveco/entreprises", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    presentation = models.TextField(blank=True, null=True)
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)
    latitude = models.FloatField()
    longitude = models.FloatField()
    telephone = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_internet = models.URLField(blank=True, null=True)
    publie = models.BooleanField(verbose_name="Publié", default=False)


class Dirigeant(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    image = FileBrowseField("Photo du dirigeant", max_length=200, directory="deveco/entreprises", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    presentation = models.TextField(blank=True, null=True)
    entreprise = models.ForeignKey(Entreprise)


class ActualiteDevEco(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image principale de l'article (facultatif)", max_length=200, directory="deveco", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié", default=False)
    date_mise_a_jour = models.DateTimeField()
    date_publication = models.DateTimeField()


class DocumentAttacheDevEco(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    document = FileBrowseField("Document", max_length=200, directory="deveco/docs", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(ActualiteDevEco)
