# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from services.models import Service



class Annonce(models.Model):
    service = models.ForeignKey(Service)
    intitule = models.CharField(max_length=255, verbose_name="Intitulé")
    slug = models.SlugField()
    type_de_poste = models.CharField(max_lenght=255, verbose_name = "Type de Poste")
    secteur_activite = models.CharField(max_lenght=255, verbose_name = "Secteur d'activité")
    niveau_formation = models.TextField(verbose_name = "Niveau de formation requis:")
    experience_requise = models.TextField(verbose_name = "Expérience requise:")
    description_du_poste = models.TextField(verbose_name = "Description du poste:")
    nom_employeur = models.TextField(verbose_name = "Nom de l'employeur:")
    provenance = models.CharField(max_length=255, verbose_name="Nom de l'employeur:")
    contact = models.TextField(verbose_name = "Contact:")
    reference = models.TextField(verbose_name = "Référence:")
    nb_postes = models.CharField(max_length=255, verbose_name="Nombre de postes:")
    deplacement = models.TextField(verbose_name = "Déplacement:")
    lieu_travail = models.TextField(verbose_name = "Lieu de travail:")
    def __unicode__(self):
        return self.nom
# Classe d'interconnexion avec l'export XLS du logiciel
# Utilisé par les maisons de l'enploi
class ImportGIDEM(models.Model):
    import = FileBrowseField("importsgidem", max_length=200, directory="documents", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])