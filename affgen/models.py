from django.db import models
from localisations.models import Ville


SEXE = (
    ('ind', u'Indeterminé'),
    ('homme', u'Homme'),
    ('femme', u'femme')
)


# Create your models here.
class Elu(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    sexe = models.CharField(max_length=5, choices=SEXE, default='ind')
    photo = models.ImageField(upload_to="cinemas", verbose_name="Photo du lieu", blank=True, null=True)
    ville = models.ForeignKey(Ville)
    publie = models.BooleanField(default=False)

    class Meta:
        ordering = ['nom']


class TitreHorsAgglo(models.Model):
    elu = models.ForeignKey(Elu)
    nom = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['index']


class QualifMandat(models.Model):
    nom = models.CharField(max_length=255)
    index = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['index']


class MandatAgglo(models.Model):
    elu = models.ForeignKey(Elu)
    nom = models.CharField(max_length=255)
    qualif = models.ForeignKey(QualifMandat)
    index = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['index']

