# -*- coding: utf-8 -*-
from evenements.models import Evenement, Organisateur, SaisonCulturelle, TypeEvenement, Festival, Prix, Tarification

from django.contrib import admin
from django.template import defaultfilters

class EvenementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'meta_description', 'description', 'image']}),
        ('Saison Culturelle', {'fields': ['cadre_evenement', 'organisateur', 'url']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Options de publication', {'fields': ['publish', 'haut_page']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish']
    filter_horizontal = ("organisateur",)

    
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

class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug=monslug)
            listsize = len(listevenement)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
        
class OrganisateurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'ville']
    fieldsets = [
        (None, {'fields': ['nom','logo','meta_description','description' ]}),
        ('Coordonnées', {'fields': ['url','email', 'telephone', 'fax', 'rue', 'ville']}),
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

class PrixAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prix', 'gratuit']
    fieldsets = [
        (None, {'fields': ['nom']}),
        ('Prix', {'fields': ['gratuit', 'prix']}),
    ]
    search_fields = ['nom']
    list_filter = ['gratuit']
    
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
admin.site.register(Prix, PrixAdmin)
admin.site.register(Tarification, TarificationAdmin)