# -*- coding: utf-8 -*-
from equipements.models import *
from django.contrib import admin
from django.template import defaultfilters
from localisations.models import Lieu

class EquipementAdmin(admin.ModelAdmin):
    list_display = ['nom_lieu', 'fonction', 'ville']
    fieldsets = [
        ('Description', {'fields': (('nom_lieu', 'fonction'), 'presentation', 'image')}),
        ('Adresse', {'fields': ['rue', 'ville', 'latitude', 'longitude']}),
        ('Contact', {'fields': ['telephone', 'fax', 'email']}),
    ]
    list_filter = ['fonction__nom', 'ville__nom']
    search_fields = ['nom_lieu']
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom_lieu)
        if obj.slug == "":
            listelieu = Lieu.objects.filter(slug=monslug)
            listsize = len(listelieu)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]

class EquipementFonctionAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ['nom']
    
    fieldsets = [
        (None, {'fields': ['nom', 'pluriel', 'picto']}),
    ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listelieu = EquipementFonction.objects.filter(slug=monslug)
            listsize = len(listelieu)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
    
class FaciliteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'importance']
    fieldsets = [
        ('Nom', {'fields': ('nom', 'description')}),
        ('Options', {'fields': ['importance', 'picto']}),
    ]
    search_fields = ['nom']
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listefacilite = Facilite.objects.filter(slug=monslug)
            listsize = len(listefacilite)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
        
class FacilitesAdmin(admin.ModelAdmin):
    list_display = ['Equipement', 'Facilites']
    search_fields = ['Equipement']
    
    filter_horizontal = ("facilites",)
    
admin.site.register(Equipement, EquipementAdmin)
admin.site.register(EquipementFonction, EquipementFonctionAdmin)
admin.site.register(Facilites, FacilitesAdmin)
admin.site.register(Facilite, FaciliteAdmin)