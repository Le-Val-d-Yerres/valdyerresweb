# -*- coding: utf-8 -*-

from editorial.models import Actualite,DocumentAttache,Magazine,PageStatique,RapportActivite
from django.contrib import admin
from django.template import defaultfilters
from valdyerresweb import settings
from valdyerresweb.utils.functions import pdftojpg
import datetime


class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 5
    max_num = 15
    



class AdminActualite(admin.ModelAdmin):
    list_display = ['titre','date_publication','publie','carroussel']
    prepopulated_fields = {'slug':('titre',),}
    fieldsets = [
        ('Page', {'fields': ['titre', 'slug', 'meta_description', 'contenu', 'image','publie']}),
        ('Date et Lieu', {'fields': ['date_publication']}),
        ('Carrousel et accueil', {
                       
                       'fields': ['carroussel','index_carroussel','page_accueil'],
                       'classes':['collapse']
                       }),
        
    ]
    inlines = [
        DocumentAttacheInline,
    ]
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.id == None:
            listsize = Actualite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.date_mise_a_jour=datetime.datetime.utcnow()
        obj.save()



class AdminPageStatique(admin.ModelAdmin):
    list_display = ['titre','date_creation','publie', 'carroussel']
    prepopulated_fields = {'slug':('titre',),}
    fieldsets = [
        ('Page', {'fields': ['titre', 'slug', 'meta_description', 'contenu', 'image','publie','note_page_accueil']}),
        ('Carrousel', {
                       
                       'fields': ['carroussel','index_carroussel'],
                       'classes':['collapse']
                       }),
        
    ]
    
    inlines = [
        DocumentAttacheInline,
    ]
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        print 
        if obj.id == None:
            listsize = Actualite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
            obj.date_creation = datetime.datetime.utcnow()
        obj.date_mise_a_jour=datetime.datetime.utcnow()
        obj.save()

    
class AdminMagazine(admin.ModelAdmin):
    list_display = ['titre','date_parution','document']
    #prepopulated_fields = {'slug':('titre',),}
    fields = ('titre','date_parution','document','publie')
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = Magazine.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        
        obj.image = pdftojpg(settings.MEDIA_ROOT+obj.document.path).replace(settings.MEDIA_ROOT,"")
        
        obj.save()
    
class AdminRapportActivite(admin.ModelAdmin):
    list_display = ['titre','date_parution','document']
    #prepopulated_fields = {'slug':('titre',),}
    fields = ('titre','date_parution','document','publie')
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = RapportActivite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.image = pdftojpg(settings.MEDIA_ROOT+obj.document.path).replace(settings.MEDIA_ROOT,"")
        obj.save()
        
        
        
admin.site.register(Actualite, AdminActualite)     
admin.site.register(PageStatique, AdminPageStatique)
admin.site.register(Magazine, AdminMagazine)
admin.site.register(RapportActivite, AdminRapportActivite)