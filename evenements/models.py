# -*- coding: utf-8 -*-
from django.db import models
from filebrowser.fields import FileBrowseField
from localisations.models import Ville, Lieu
from model_utils.managers import InheritanceManager
from services.models import Service
from equipements.models import Equipement
from localisations.models import Ville
from django.db.models import permalink
from django.template import defaultfilters


class Organisateur(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    meta_description = models.CharField(max_length=200)
    description = models.TextField()
    logo = FileBrowseField("Image", max_length=255, directory="evenements",
                           extensions=[".jpg", ".png", ".gif", ".jpeg"], blank=True, null=True)
    url = models.URLField("Site de cet organisateur:  (facultatif) ", blank=True)
    email = models.EmailField("Mail (facultatif)", max_length=255, blank=True)
    telephone = models.CharField(max_length=25)
    fax = models.CharField("Fax (facultatif)", max_length=25, blank=True)
    rue = models.CharField(max_length=255)
    ville = models.ForeignKey(Ville)

    # Un choix de design pas très beau, mais fonctionellement les équipements, services, communes de la
    # communauté d'agglo peuvent organiser des evènements ainsi que d'autres entités exterieures alors ...

    orga_service = models.ForeignKey(Service, blank=True, null=True)
    orga_equipement = models.ForeignKey(Equipement, blank=True, null=True)
    orga_ville = models.ForeignKey(Ville, blank=True, null=True, related_name='orga_orga_ville')

    def __unicode__(self):
        return self.nom + " / " + self.ville.nom

    class Meta:
        verbose_name_plural = "Organisateurs"
        ordering = ['ville__nom']


class Saison(models.Model):
    nom = models.CharField(max_length=255)
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("date de fin")
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)

    objects = InheritanceManager()

    def __unicode__(self):
        return self.nom


class SaisonCulturelle(Saison):
    def __unicode__(self):
        return self.nom


class Festival(Saison):
    saison_culture = models.ForeignKey(SaisonCulturelle)

    def __unicode__(self):
        return self.nom


class TypeEvenement(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.nom


EVENEMENT_CATEGORIES = (
    ('bib', u'Bibliothèques/Médiatèques'),
    ('crd', u'Conservatoires'),
    ('sty', u'Sothevy'),
    ('aut', u'Autres'),
)


class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=200)
    description = models.TextField()
    debut = models.DateTimeField("Date de début", blank=True, null=True)
    fin = models.DateTimeField("Date de fin", blank=True, null=True)
    organisateur = models.ManyToManyField(Organisateur)
    image = FileBrowseField("Image", max_length=255, directory="evenements",
                            extensions=[".jpg", ".png", ".gif", ".jpeg", ".pdf"], blank=True, null=True)
    url = models.URLField("Un lien vers plus d'infos: (facultatif)", blank=True, null=True)
    url_reservation = models.URLField(
        "Un lien vers la page de reservation: (facultatif, annule le lien vers plus d'infos) ", blank=True, null=True)
    categorisation = models.CharField(max_length=3, choices=EVENEMENT_CATEGORIES, default='aut')
    cadre_evenement = models.ForeignKey(Saison)
    type = models.ForeignKey(TypeEvenement)
    lieu = models.ForeignKey(Lieu, blank=True, null=True)
    publish = models.BooleanField("Publié", default=False)
    page_accueil = models.BooleanField("Page d'accueil", default=False)
    complet = models.BooleanField("Ce spectacle est complet", default=False)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['-debut']

    def Organisateurs(self):
        return "\n;\n".join([s.nom for s in self.organisateur.all()])

    def dates(self):
        return "\n;\n".join([s.debut.strftime('%d-%m-%Y %H:%M') for s in self.datelieuevenement_set.all().order_by('fin')])


    def __unicode__(self):
        return self.nom

    def monthyeardebut(self):
        return self.debut.strftime("%m") + "-" + self.debut.strftime("%Y")

    @permalink
    def get_absolute_url(self):
        return ('event-details', (), {'slug': self.cadre_evenement.slug, 'evenement_slug': self.slug})




class DateLieuEvenement(models.Model):
    debut = models.DateTimeField("Date de début")
    fin = models.DateTimeField("Date de fin")
    lieu = models.ForeignKey(Lieu)
    evenement = models.ForeignKey(Evenement)

    class Meta:
        verbose_name_plural = u"Dates et Lieux"
        verbose_name = u"Date et Lieu"


class Prix(models.Model):
    intitule = models.CharField("Intitulé ", max_length=255, blank=False, null=False)
    prix = models.FloatField("Prix (séparateur point ex : 0.5 )", default=None, blank=False, null=True)
    evenement = models.ForeignKey(Evenement)

    class Meta:
        verbose_name_plural = u"Prix"


class DocumentAttache(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    document = FileBrowseField("Document", max_length=200, directory="evenements/docs",
                               extensions=[".pdf", ".doc", ".odt", ".docx", ".txt"])
    reference = models.ForeignKey(Evenement)


class EvenementBibManager(models.Manager):
    def get_queryset(self):
        return super(EvenementBibManager, self).get_queryset().filter(
            categorisation='bib')


class EvenementBib(Evenement):
    objects = EvenementBibManager()

    class Meta:
        proxy = True
        verbose_name_plural = u"Événements Bibliothèques"
        verbose_name = u"Événement Bibliothèque"

    def save(self, *args, **kwargs):
        self.categorisation = 'bib'
        super(Evenement, self).save(*args, **kwargs)

