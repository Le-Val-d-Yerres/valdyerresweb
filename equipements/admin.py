# -*- coding: utf-8 -*-
from equipements.models import Equipement, EquipementFonction
from django.contrib import admin

class EquipementAdmin(admin.ModelAdmin):
    list_display = ['nom_lieu', 'fonction', 'ville']
    fieldsets = [
        ('Description', {'fields': ['nom_lieu', 'fonction', 'presentation', 'image']}),
        ('Adresse', {'fields': ['rue', 'ville', 'latitude', 'longitude']}),
        ('Contact', {'fields': ['telephone', 'fax', 'email']}),
    ]
    list_filter = ['fonction__nom', 'ville__nom']
    search_fields = ['nom_lieu']

class EquipementFonctionAdmin(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ['nom']
    
admin.site.register(Equipement, EquipementAdmin)
admin.site.register(EquipementFonction, EquipementFonctionAdmin)