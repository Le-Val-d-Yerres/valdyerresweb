# -*- coding: utf-8 -*-

from django.db import models
from localisations.models import Ville


SEXE = (
    ('ind', u'Indeterminé'),
    ('homme', u'Homme'),
    ('femme', u'Femme')
)


# Create your models here.
class Elu(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    sexe = models.CharField(max_length=5, choices=SEXE, default='ind')
    photo = models.ImageField(upload_to="affgen", verbose_name="Photo", blank=True, null=True)
    ville = models.ForeignKey(Ville)
    publie = models.BooleanField(default=False,verbose_name=u"Publié")

    class Meta:
        ordering = ['nom']

    def __unicode__(self):
        return self.nom


class TitreHorsAgglo(models.Model):
    elu = models.ForeignKey(Elu)
    nom = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField(verbose_name="ordre d'apparition")

    class Meta:
        ordering = ['index']


class QualifMandat(models.Model):
    nom = models.CharField(max_length=255)
    feminin = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField(verbose_name="ordre d'apparition")

    class Meta:
        ordering = ['index']

    def __unicode__(self):
        return self.nom


class MandatAgglo(models.Model):
    elu = models.ForeignKey(Elu)
    nom = models.CharField(max_length=255)
    qualif = models.ForeignKey(QualifMandat)
    index = models.PositiveSmallIntegerField(verbose_name="ordre d'apparition")

    class Meta:
        ordering = ['index']
        verbose_name = u"Mandat dans l'agglo"
        verbose_name_plural = u"Mandats dans l'agglo"

