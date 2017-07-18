# -*- coding: utf-8 -*-

from django.db import models


class Disciplinestagecrd(models.Model):
    nom = models.CharField(max_length=255)
    index = models.IntegerField()

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "discipline stage"
        verbose_name_plural = 'disciplines stage'
        ordering = ['index']


class Fichestagecrd(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    commentaires = models.TextField(null=True)
    choix_1 = models.ForeignKey(Disciplinestagecrd,related_name="choix_1", null=True)
    choix_2 = models.ForeignKey(Disciplinestagecrd,related_name="choix_2", null=True)
    choix_3 = models.ForeignKey(Disciplinestagecrd,related_name="choix_3", null=True)

    class Meta:
        verbose_name = "fiche stage"
        verbose_name_plural = 'fiches stage'
        ordering = ['nom']

    def __str__(self):
        return self.nom


class Intitulestage(models.Model):
    nom = models.CharField(max_length=255)
    duree = models.CharField(max_length=255)
    index = models.IntegerField()

    class Meta:
        verbose_name = u"intitulé stage"
        verbose_name_plural = u"intitulés stage"
        ordering = ['index']

    def __str__(self):
        return self.nom


class Stage(models.Model):
    intitule = models.ForeignKey(Intitulestage)
    fiche = models.ForeignKey(Fichestagecrd)
    toussaint_1 = models.BooleanField(default=False)
    toussaint_2 = models.BooleanField(default=False)
    hiver_1 = models.BooleanField(default=False)
    hiver_2 = models.BooleanField(default=False)
    paques_1 = models.BooleanField(default=False)
    paques_2 = models.BooleanField(default=False)
    ete_1 = models.BooleanField(default=False)
    ete_2 = models.BooleanField(default=False)
