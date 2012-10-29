from django.db import models
from filebrowser.fields import FileBrowseField
# Create your models here.

class SectionPage(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")

class Categorie(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    parent = models.ForeignKey('self', null= True,blank=True)
    
    def __unicode__(self):
        return self.nom
    

class PageBase(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    slug = models.SlugField()
    meta_description = models.CharField(max_length=200)
    contenu = models.TextField()
    publie = models.BooleanField()

class PageStatique(PageBase):
    categorie = models.ForeignKey(Categorie)
    
class Actualite(PageBase):
    date_publication = models.DateTimeField()

    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageStatique)
    
class Magazine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf"])
     
class RapportActivite(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf"])