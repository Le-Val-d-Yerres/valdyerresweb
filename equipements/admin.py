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
        ('Classification', {'fields': ['type']}),
        ('Alerte', {'fields': ['alerte']}),
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
        
        path = reverse('equipement-details', kwargs={'fonction_slug':obj.fonction.slug,'equipement_slug':obj.slug})
        functions.expire_page(path)
        
        path = reverse('equipements-carte', kwargs={})
        functions.expire_page(path)

        path = reverse('equipement-vcf', kwargs={'slug':obj.slug})
        functions.expire_page(path)
        
    
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

class EquipementFonctionAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ['nom']
    
    fieldsets = [
        (None, {'fields': ['nom', 'pluriel', 'picto','logo','service','schema_url']}),
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
        
        path = reverse('equipements-carte', kwargs={})
        functions.expire_page(path)

        path = reverse('onction-details-html', kwargs={'fonction_slug':obj.slug})
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
        
        path = reverse('facilite-liste', kwargs={})
        functions.expire_page(path)

        path = reverse('facilite-carte', kwargs={'slug':obj.slug})
        functions.expire_page(path)
        
class FacilitesAdmin(admin.ModelAdmin):
    list_display = ['Equipement', 'Facilites']
    search_fields = ['Equipement']
    filter_horizontal = ("facilites",)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('facilite-liste', kwargs={})
        functions.expire_page(path)
    

class TarifCategorieAdmin(admin.ModelAdmin):
    list_display = ['equipement_fonction','nom']
    prepopulated_fields = {'slug':('nom',),}
    
    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('equipement-tarifs', kwargs={})
        functions.expire_page(path)
    
    
class TarifAdmin(admin.ModelAdmin):
    list_display = ['designation', 'categorie', 'prix_residents', 'prix_non_residents', 'index']
    
    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('equipement-tarifs', kwargs={})
        functions.expire_page(path)


class TarifSpecifiqueAdmin(admin.ModelAdmin):
    list_display = ['designation', 'equipement', 'categorie', 'prix_residents', 'prix_non_residents', 'index']

    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('equipement-tarifs', kwargs={})
        functions.expire_page(path)
        
class AlerteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'texte_lien']
    search_fields = ['nom']
    
class AlertesReponsesAdmin(admin.ModelAdmin):
    list_display = ['alerte', 'equipement', 'nom', 'prenom', 'date', 'etat']
    list_filter = ['etat', 'equipement']
    search_fields = ['equipement_id']

admin.site.register(Equipement, EquipementAdmin)
admin.site.register(EquipementFonction, EquipementFonctionAdmin)
admin.site.register(Facilites, FacilitesAdmin)
admin.site.register(Facilite, FaciliteAdmin)
admin.site.register(TarifCategorie, TarifCategorieAdmin)
admin.site.register(Tarif, TarifAdmin)
admin.site.register(TarifSpecifique, TarifSpecifiqueAdmin)
admin.site.register(Alerte, AlerteAdmin)
admin.site.register(AlertesReponses, AlertesReponsesAdmin)
