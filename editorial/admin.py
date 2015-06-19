# -*- coding: utf-8 -*-

from editorial.models import Actualite, DocumentAttache, Magazine, PageStatique, RapportActivite, NewsletterBib
from equipements.models import Equipement
from django.contrib import admin
from django.template import defaultfilters
from valdyerresweb import settings
from valdyerresweb.utils.functions import pdftojpg
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse
from django import forms

import datetime


class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 5
    max_num = 15


class AdminActualite(admin.ModelAdmin):
    search_fields = ['titre']
    list_display = ['titre', 'date_publication', 'publie', 'carroussel']
    prepopulated_fields = {'slug': ('titre',), }
    fieldsets = [
        ('Page', {'fields': ['titre', 'slug', 'meta_description', 'contenu', 'image', 'publie']}),
        ('Date et Lieu', {'fields': ['date_publication']}),
        ('Carrousel et accueil', {

            'fields': ['carroussel', 'index_carroussel', 'page_accueil'],
            'classes': ['collapse']
        }),

    ]
    inlines = [
        DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.id == None:
            listsize = Actualite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
        obj.date_mise_a_jour = datetime.datetime.utcnow()
        obj.save()

        path = reverse('editorial.views.Home', kwargs={})
        functions.expire_page(path)

        path = reverse('editorial.views.ActuList', kwargs={})
        functions.expire_page(path)

        path = reverse('editorial.views.ActuDetail', kwargs={'actualite_slug': obj.slug})
        functions.expire_page(path)


class AdminPageStatique(admin.ModelAdmin):
    list_display = ['titre', 'date_creation', 'publie', 'carroussel']
    prepopulated_fields = {'slug': ('titre',), }
    fieldsets = [
        ('Page', {'fields': ['titre', 'slug', 'meta_description', 'contenu', 'image', 'publie', 'note_page_accueil']}),
        ('Carrousel', {

            'fields': ['carroussel', 'index_carroussel'],
            'classes': ['collapse']
        }),

    ]

    inlines = [
        DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        print
        if obj.id == None:
            listsize = Actualite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
            obj.date_creation = datetime.datetime.utcnow()
        obj.date_mise_a_jour = datetime.datetime.utcnow()
        obj.save()

        path = reverse('editorial.views.PageDetail', kwargs={'page_slug': obj.slug})
        functions.expire_page(path)


class AdminMagazine(admin.ModelAdmin):
    list_display = ['titre', 'date_parution', 'document']
    # prepopulated_fields = {'slug':('titre',),}
    fields = ('titre', 'date_parution', 'document', 'publie')

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = Magazine.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug

        obj.image = pdftojpg(settings.MEDIA_ROOT + obj.document.path).replace(settings.MEDIA_ROOT, "")

        obj.save()

        path = reverse('editorial.views.Magazines', kwargs={})
        functions.expire_page(path)


class AdminRapportActivite(admin.ModelAdmin):
    list_display = ['titre', 'date_parution', 'document']
    # prepopulated_fields = {'slug':('titre',),}
    fields = ('titre', 'date_parution', 'document', 'publie')

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = RapportActivite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
        obj.image = pdftojpg(settings.MEDIA_ROOT + obj.document.path).replace(settings.MEDIA_ROOT, "")
        obj.save()

        path = reverse('editorial.views.Rapports', kwargs={})
        functions.expire_page(path)


class NewsletterBibForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterBibForm, self).__init__(*args, **kwargs)
        self.fields['bib'].queryset = Equipement.objects.filter(type="bib")

class AdminNewsletterBib(admin.ModelAdmin):
    list_display = ['maj', 'bib', 'evenement_debut', 'evenement_fin']
    fields = ('bib', 'edito', 'evenement_debut', 'evenement_fin')
    form = NewsletterBibForm

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('editorial.views.newsletterbibhtml', kwargs={'equipement_slug': obj.bib.slug})
        functions.expire_page(path)


admin.site.register(Actualite, AdminActualite)
admin.site.register(PageStatique, AdminPageStatique)
admin.site.register(Magazine, AdminMagazine)
admin.site.register(RapportActivite, AdminRapportActivite)
admin.site.register(NewsletterBib, AdminNewsletterBib)
