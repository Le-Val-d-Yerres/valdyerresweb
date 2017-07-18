# -*- coding: utf-8 -*-

from django.db import models
from filebrowser.fields import FileBrowseField
from model_utils.managers import InheritanceManager
from django.db.models import permalink
from django.db import models
from django.urls import reverse

# Create your models here.
from equipements.models import Equipement


class PageBase(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    meta_description = models.CharField(max_length=200)
    image = FileBrowseField("Image principale de l'article (facultatif)", max_length=200, directory="editorial", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    contenu = models.TextField()
    publie = models.BooleanField(verbose_name="Publié", default=False)
    date_mise_a_jour = models.DateTimeField()
    carroussel = models.BooleanField("Présence dans le carroussel de la page d'accueil",default=False)
    index_carroussel = models.IntegerField("Ordre d'affichage dans le caroussel (0 = premier)",default=0)
    objects = InheritanceManager()


class PageStatique(PageBase):
    date_creation = models.DateTimeField()
    note_page_accueil = models.BooleanField("Lister dans les notes de la page d'accueil", default=False)

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'page_slug': self.slug})


class Actualite(PageBase):
    
    date_publication = models.DateTimeField()
    page_accueil = models.BooleanField("Affichage en page d'accueil ?", default=False)

    def get_absolute_url(self):
        return reverse('actudetail', kwargs={'actualite_slug': self.slug})
   
    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="editorial/docs", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageBase)


class Magazine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField(max_length=255)
    date_parution = models.DateField()
    document = FileBrowseField("Document PDF", max_length=200, directory="magazines", extensions=[".pdf"])
    image = models.ImageField(upload_to="magazines/img",blank=True)
    publie = models.BooleanField(verbose_name="Publié", default=False)

     
class RapportActivite(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre", blank = True) # a supprimer
    slug = models.SlugField(max_length=255)
    date_parution = models.DateField()
    document = FileBrowseField("Document PDF", max_length=200, directory="rapports", extensions=[".pdf"])
    image = models.ImageField(upload_to="rapports/img") 
    publie = models.BooleanField(verbose_name="Publié", default=False)

class NewsletterBib(models.Model):
    maj = models.DateField(auto_now=True, verbose_name='Date de mise à jour')
    edito = models.TextField(verbose_name="Edito",blank=True)
    evenement_debut = models.DateField("Date de Début des événements")
    evenement_fin = models.DateField("Date de fin des événements")
    bib = models.ForeignKey(Equipement)

    def get_absolute_url(self):
        return reverse('newsletterbibhtml',  kwargs={'equipement_slug': self.bib.slug})
