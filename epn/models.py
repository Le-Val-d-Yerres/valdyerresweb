from django.db import models
from django.utils import timezone
from uuid import uuid4

class FicheInscription(models.Model):
    homme = "H"
    femme = "F"
    SEXE_CHOICES = (
        (homme, 'Homme'),
        (femme, 'Femme')
    )
    adultereferent = models.ForeignKey("self", models.SET_NULL, null=True, blank=True, default=None)
    uuid = models.CharField(max_length=36, default=None, null=True, editable=False)
    dateinscription = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    datenaissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default=femme)
    email = models.EmailField()
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
