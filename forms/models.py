from django.db import models


class Disciplinestagecrd(models.Model):
    nom = models.CharField(max_length=255)
    index = models.IntegerField()


class Fichestagecrd(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    commentaires = models.TextField(null=True)


class Stage(models.Model):
    nom = models.CharField(max_length=255)
    duree = models.CharField(max_length=255)
    toussaint_1 = models.BooleanField(default=False)
    toussaint_2 = models.BooleanField(default=False)
    hiver_1 = models.BooleanField(default=False)
    hiver_2 = models.BooleanField(default=False)
    paques_1 = models.BooleanField(default=False)
    paques_2 = models.BooleanField(default=False)
    ete_1 = models.BooleanField(default=False)
    ete_2 = models.BooleanField(default=False)
    fiche = models.ForeignKey(Fichestagecrd)