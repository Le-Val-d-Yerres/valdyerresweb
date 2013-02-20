# -*- coding: utf-8 -*-
from evenements.models import Evenement, Organisateur, SaisonCulturelle, TypeEvenement, Festival, Prix, DocumentAttache
from valdyerresweb.utils.functions import pdftojpg
from django.contrib import admin
from django.template import defaultfilters
from valdyerresweb import settings
import os

class PrixInline(admin.TabularInline):
    model = Prix
    extra = 2
    max_num = 15

class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 2
    max_num = 15
    
class EvenementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'meta_description', 'description', 'image']}),
        ('Saison Culturelle', {'fields': ['cadre_evenement', 'organisateur', 'url', 'url_reservation']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Option de publication', {'fields': ['publish','complet','page_accueil']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish']
    filter_horizontal = ("organisateur",)

    inlines = [
        PrixInline,DocumentAttacheInline,
    ]
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
        
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug=monslug)
            listsize = len(listevenement)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg( os.path.join(settings.MEDIA_ROOT,obj.image.path), subpath="")
                obj.image = os.path.relpath(abspath_image, settings.MEDIA_ROOT) 
        obj.save()

class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']
    prepopulated_fields = {'slug':('nom',),}
    
        
class OrganisateurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'ville']
    fieldsets = [
        (None, {'fields': ['nom','logo','meta_description','description' ]}),
        ('Coordonnées', {'fields': ['url','email', 'telephone', 'fax', 'rue', 'ville']}),
        ('Entitées liées',{'fields':['orga_service','orga_equipement','orga_ville']})
    ]
    list_filter = ['ville__nom']
    search_fields = ['nom']
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug=monslug)
            listsize = len(listevenement)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
    
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['nom', 'saison_culture', 'debut', 'fin']
    fieldsets = [
        (None, {'fields': ['nom', 'description', 'saison_culture']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    list_filter = ['saison_culture__nom']
    search_fields = ['nom']
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listefestival = Festival.objects.filter(slug=monslug)
            listsize = len(listefestival)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
    
class SaisonCulturelleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'debut', 'fin']
    fieldsets = [
        (None, {'fields': ['nom', 'description']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    search_fields = ['nom']
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listesaisonculturelle = SaisonCulturelle.objects.filter(slug=monslug)
            listsize = len(listesaisonculturelle)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()

class TarificationAdmin(admin.ModelAdmin):
    list_display = ['Evenement', 'Prix']
    fieldsets = [
        ('Evènement', {'fields': ['evenement']}),
        ('Prix', {'fields': ['prix']}),
    ]
    filter_horizontal = ("prix",)

admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Organisateur, OrganisateurAdmin)
admin.site.register(SaisonCulturelle, SaisonCulturelleAdmin)
admin.site.register(TypeEvenement,TypeEvenementAdmin)
admin.site.register(Festival, FestivalAdmin)
