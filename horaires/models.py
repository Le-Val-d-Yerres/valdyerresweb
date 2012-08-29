# -*- coding: utf-8 -*-
from django.db import models
from equipements.models import Equipement

# Create your models here.

class Horaires(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Nom de la période")
    equipement = models.ForeignKey(Equipement)
    date_debut = models.DateField(u"Début de la période")
    date_fin = models.DateField(u"Fin de la période")
   # lundi_matin_debut = DateTimeField()
    