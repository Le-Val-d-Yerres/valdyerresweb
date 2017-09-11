from django.db import models


class FicheInscription(models.Model):
    homme = "H"
    femme = "F"
    SEXE_CHOICES = (
        (homme, 'Homme'),
        (femme, 'Femme')
    )

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
