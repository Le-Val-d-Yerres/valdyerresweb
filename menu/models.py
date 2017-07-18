# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class MenuItem(models.Model):
    nom = models.CharField(max_length=255)
    chemin = models.CharField(max_length=255)
    index  = models.IntegerField()
    parent = models.ForeignKey('self', null= True,blank=True)
    
    def __str__(self):
        return self.nom