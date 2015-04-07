# -*- coding: utf-8 -*-
from localisations.models import Ville, Lieu
from django.contrib import admin
from django.template import defaultfilters
from django.utils.timezone import utc
import datetime
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse
    
class LieuAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville']
    fieldsets = [
        (None, {'fields': ['nom' ]}),
        ('Adresse', {'fields': ['rue', 'ville']}),
        ('Coordonnées GPS', {'fields': ['latitude', 'longitude']}),
    ]
    list_filter = ['ville__nom']
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
        
        today = datetime.datetime.utcnow().replace(tzinfo=utc)
        functions.resetEphemerideCache(today)
        
    
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
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

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