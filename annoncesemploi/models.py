# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from services.models import Service
import xlrd



class Annonce(models.Model):
    service = models.ForeignKey(Service,null=True)
    publie = models.BooleanField(verbose_name = "Publié:")
    intitule = models.CharField(max_length=255, verbose_name="Intitulé:")
    slug = models.SlugField()
    type_de_poste = models.CharField(max_lenght=255, verbose_name = "Type de Poste:")
    secteur_activite = models.CharField(max_lenght=255, verbose_name = "Secteur d'activité:")
    niveau_formation = models.TextField(verbose_name = "Niveau de formation requis:")
    experience_requise = models.TextField(verbose_name = "Expérience requise:")
    description_du_poste = models.TextField(verbose_name = "Description du poste:")
    nom_employeur = models.TextField(verbose_name = "Nom de l'employeur:")
    contact = models.TextField(verbose_name = "Contact:")
    nb_postes = models.CharField(max_length=255, verbose_name="Nombre de postes:")
    deplacement = models.TextField(verbose_name = "Déplacement:")
    lieu_travail = models.TextField(verbose_name = "Lieu de travail:")
    salaire_indicatif = models.CharField(max_length=255, verbose_name = "Salaire indicatif:")
    def __unicode__(self):
        return self.nom
    

# Classe d'interconnexion avec l'export XLS du logiciel
# utilisé par les maisons de l'emploi
class ImportGIDEM(models.Model):
    fichier_xls = FileBrowseField("Document", max_length=200, directory="importsgidem", extensions=[".xls"])
    date_import = models.DateTimeField()
    
    def parseimport(self,filename):
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        annonce = Annonce()
        for row in range(1,worksheet.nrows):
            annonce.intitule = worksheet.cell(row,2).value.lower().capitalize()
            annonce.type_de_poste = worksheet.cell(row,7).value
            annonce.secteur_activite = worksheet.cell(row,4).value
            annonce.niveau_formation = worksheet.cell(row,10).value
            annonce.experience_requise = worksheet.cell(row,9).value
            annonce.description_du_poste = worksheet.cell(row,8).value
            annonce.nom_employeur = worksheet.cell(row,5).value
            annonce.contact = worksheet.cell(row,6).value
            annonce.nbpostes = worksheet.cell(row,11).value
            annonce.deplacement = worksheet.cell(row,15).value
            annonce.lieu_travail = worksheet.cell(row,12).value
            annonce.salaire_indicatif = worksheet.cell(row,14).value
            
        
        