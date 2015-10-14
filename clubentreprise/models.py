from django.db import models
from localisations.models import Ville


class Entreprise(models.Model):
    nom = models.CharField(max_length=255)
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)
    email = models.EmailField(blank=True, null=True)
    site_internet = models.URLField(blank=True, null=True)


class Dirigeant(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    presentation = models.TextField(blank=True, null=True)
    entreprise = models.ForeignKey(Entreprise)
