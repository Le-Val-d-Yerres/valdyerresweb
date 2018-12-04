from django.db import models
from localisations.models import Lieu
from filebrowser.fields import FileBrowseField
# Create your models here.

class Site(Lieu):
    presentation = models.TextField(blank=True)
    meta_description = models.CharField(max_length=200)
    alerte = models.ForeignKey(Alerte, blank=True, null=True, default=None)
    image = FileBrowseField("Image (facultatif)", max_length=200, directory="equipements",
                            extensions=[".jpg", ".png", ".gif", ".jpeg"], blank=True, null=True)

    def __str__(self):
        return self.ville.nom + " - " + self.nom

    class Meta:
        ordering = ('ville__nom',)

    @permalink
    def get_absolute_url(self):
        return ('site', (), {'site_slug': self.slug})