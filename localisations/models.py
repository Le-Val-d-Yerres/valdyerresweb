# -*- coding: utf-8 -*-
from django.db import models
from model_utils.managers import InheritanceManager

class Ville(models.Model):
    nom = models.CharField(max_length=150)
    code_postal = models.CharField(max_length=10)
    communaute_agglo = models.BooleanField(default=False)
    description = models.TextField()
    lien = models.URLField()
    meta_description = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Villes"
        ordering = ['nom']


class Lieu(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)
    latitude = models.FloatField()
    longitude = models.FloatField()
    slug = models.SlugField(max_length=255, unique=True)
    
    objects = InheritanceManager()
    
    def __str__(self):
        return self.ville.nom+" | "+self.nom + " | "+self.rue

    class Meta:
        verbose_name_plural = "Lieux"
        ordering = ['ville__nom','nom']
