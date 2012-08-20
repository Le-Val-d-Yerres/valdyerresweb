# -*- coding: utf-8 -*-
from localisations.models import Ville, Lieu
from django.contrib import admin
from django.template import defaultfilters
    
class LieuAdmin(admin.ModelAdmin):
    list_display = ['nom_lieu', 'ville']
    fieldsets = [
        (None, {'fields': ['nom_lieu' ]}),
        ('Adresse', {'fields': ['rue', 'ville']}),
        ('Coordonnées GPS', {'fields': ['latitude', 'longitude']}),
    ]
    list_filter = ['ville__nom']
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
    
class VilleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'lien', 'communaute_agglo']
    fieldsets = [
        ('Coordonnées', {'fields': ['nom', 'code_postal', 'communaute_agglo']}),
        ('Description', {'fields': ['description', 'meta_description', 'lien']}),
    ]
    list_filter = ['communaute_agglo']
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
            listeville = Ville.objects.filter(slug=monslug)
            listsize = len(listeville)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()

admin.site.register(Ville, VilleAdmin)
admin.site.register(Lieu, LieuAdmin)