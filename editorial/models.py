from django.db import models
from filebrowser.fields import FileBrowseField
# Create your models here.


class Categorie(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    slug = models.SlugField()
    index  = models.IntegerField()
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
    logo = FileBrowseField("Logo de l'article (facultatif)", max_length=200, directory="equipements", extensions=[".jpg", ".png", ".giff", ".jpeg"], blank=True, null=True)
    date_publication = models.DateTimeField()
    page_accueil = models.BooleanField()
    
class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom") 
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(PageBase)
    
class Magazine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf"])
    image = models.ImageField()
     
class RapportActivite(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre")
    date_parution = models.DateField()
    document = FileBrowseField("Document", max_length=200, directory="documents", extensions=[".pdf"])
    image = models.ImageField()