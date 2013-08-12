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
        ('Description', {'fields': (('nom', 'fonction'),'meta_description', 'presentation', 'image', 'url')}),
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
        
        path = reverse('equipements.views.EquipementsCarte', kwargs={})
        functions.expire_page(path)

        path = reverse('equipements.views.EquipementVCF', kwargs={'slug':obj.slug})
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
        
        path = reverse('equipements.views.EquipementsCarte', kwargs={})
        functions.expire_page(path)

        path = reverse('equipements.views.FonctionDetailsHtml', kwargs={'fonction_slug':obj.slug})
        functions.expire_page(path)
    
class FaciliteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'importance']
    fieldsets = [
        ('Nom', {'fields': ('nom','slug', 'description')}),
        ('Attributs', {'fields': ['importance', 'picto','picto_geoloc']}),
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
        
        path = reverse('equipements.views.FaciliteListe', kwargs={})
        functions.expire_page(path)

        path = reverse('equipements.views.FaciliteCarte', kwargs={'slug':obj.slug})
        functions.expire_page(path)
        
class FacilitesAdmin(admin.ModelAdmin):
    list_display = ['Equipement', 'Facilites']
    search_fields = ['Equipement']
    filter_horizontal = ("facilites",)
    
    def save_model(self, request, obj, form, change):
        path = reverse('equipements.views.FaciliteListe', kwargs={})
        functions.expire_page(path)
    

class TarifCategorieAdmin(admin.ModelAdmin):
    list_display = ['equipement_fonction','nom']
    prepopulated_fields = {'slug':('nom',),}
    
    # TODO : ajouter la suppression du cache de la page "equipements/tarifs/" quand elle sera ajouté
    
    
class TarifAdmin(admin.ModelAdmin):
    list_display = ['designation','categorie', 'index']
    
    # TODO : ajouter la suppression du cache de la page "equipements/tarifs/" quand elle sera ajouté

admin.site.register(Equipement, EquipementAdmin)
admin.site.register(EquipementFonction, EquipementFonctionAdmin)
admin.site.register(Facilites, FacilitesAdmin)
admin.site.register(Facilite, FaciliteAdmin)
admin.site.register(TarifCategorie, TarifCategorieAdmin)
admin.site.register(Tarif, TarifAdmin)
