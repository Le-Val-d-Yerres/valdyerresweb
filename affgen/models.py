# -*- coding: utf-8 -*-

from django.db import models
from localisations.models import Ville
from filebrowser.fields import FileBrowseField


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

    def __str__(self):
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

    def __str__(self):
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


ENTITE = (
    ('vyvs', u'Val d’Yerres Val de Seine'),
    ('casvs', u'Val de Seine'),
    ('cavy', u'Val d’Yerres')
)


class Cptrendu(models.Model):
    date = models.DateField(verbose_name="Date du conseil")
    entite = models.CharField(max_length=5, choices=ENTITE, default='vyvs')
    document = models.FileField("Document PDF", max_length=200,  upload_to="uploads/comptesrendus")

    class Meta:
        ordering = ['-date']
        verbose_name = u"Compte rendu conseil"
        verbose_name_plural = u"Comptes rendus"

    def deliberations(self):
        return Deliberation.objects.all().filter(compterendu=self.id)

class Deliberation(models.Model):
    compterendu = models.ForeignKey(Cptrendu)
    numreference = models.CharField(verbose_name="Numéro de référence", max_length=32)
    titre = models.CharField(max_length=255)
    document = models.FileField("Fichier PDF", upload_to="uploads/deliberations/")

    class Meta:
        ordering = ['numreference']
        verbose_name = u"Délibération"
        verbose_name_plural = u"Délibérations"




