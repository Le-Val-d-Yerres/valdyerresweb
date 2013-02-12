# -*- coding: utf-8 -*-
from equipements.models import *
from django.contrib import admin
from django.template import defaultfilters
from localisations.models import Lieu
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse

class EquipementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'fonction', 'ville']
    fieldsets = [
        ('Description', {'fields': (('nom', 'fonction'), 'presentation', 'image', 'url')}),
        ('Adresse', {'fields': ['rue', 'ville', 'latitude', 'longitude']}),
        ('Contact', {'fields': ['telephone', 'fax', 'email']}),
    ]
    list_filter = ['fonction__nom', 'ville__nom']
    search_fields = ['nom']
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listelieu = Lieu.objects.filter(slug=monslug)
            listsize = len(listelieu)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
        path = reverse('equipements.views.EquipementsDetailsHtml', kwargs={'fonction_slug':obj.fonction.slug,'equipement_slug':obj.slug})
        functions.expire_page(path)
    
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
        (None, {'fields': ['nom', 'pluriel', 'picto','logo','service']}),
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
    

class TarifCategorieAdmin(admin.ModelAdmin):
    list_display = ['equipement_fonction','nom']
    prepopulated_fields = {'slug':('nom',),}
    
    
class TarifAdmin(admin.ModelAdmin):
    list_display = ['designation','categorie', 'index']

admin.site.register(Equipement, EquipementAdmin)
admin.site.register(EquipementFonction, EquipementFonctionAdmin)
admin.site.register(Facilites, FacilitesAdmin)
admin.site.register(Facilite, FaciliteAdmin)
admin.site.register(TarifCategorie, TarifCategorieAdmin)
admin.site.register(Tarif, TarifAdmin)