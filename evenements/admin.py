# -*- coding: utf-8 -*-
from evenements.models import Evenement, Contact, SaisonCulturelle, TypeEvenement, Festival
from django.contrib import admin
from django.template import defaultfilters

class EvenementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'Lieu', 'debut', 'fin']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'meta_description', 'description', 'image', 'url', 'contact']}),
        ('Saison Culturelle', {'fields': ['cadre_evenement', 'communal', 'communautaire']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
    ]
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

    
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'ville']
    fieldsets = [
        (None, {'fields': ['nom' ]}),
        ('Coordonnées', {'fields': ['email', 'telephone', 'fax', 'rue', 'ville']}),
    ]
    list_filter = ['ville__nom']
    search_fields = ['nom']
    
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['nom', 'saison_culture', 'debut', 'fin']
    fieldsets = [
        (None, {'fields': ['nom', 'saison_culture']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    list_filter = ['saison_culture__nom']
    search_fields = ['nom']
    
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
        (None, {'fields': ['nom']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    search_fields = ['nom']
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listesaisonculturelle = SaisonCulturelle.objects.filter(slug=monslug)
            listsize = len(listesaisonculturelle)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()

admin.site.register(Evenement, EvenementAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(SaisonCulturelle, SaisonCulturelleAdmin)
admin.site.register(TypeEvenement)
admin.site.register(Festival, FestivalAdmin)