# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Aide(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField()
    contenu = models.TextField()  
    def unicode(self):
        return self.nom

