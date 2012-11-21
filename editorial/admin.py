# -*- coding: utf-8 -*-

from editorial.models import Actualite,DocumentAttache,Magazine,PageStatique,RapportActivite
from django.contrib import admin
from django.template import defaultfilters
from valdyerresweb import settings
import ghostscript

class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 5
    max_num = 15


class AdminActualite(admin.ModelAdmin):
    list_display = ['titre','date_publication','publie']
    prepopulated_fields = {'slug':('titre',),}
    inlines = [
        DocumentAttacheInline,
    ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.intitule)
        if obj.slug == "":
            listsize = Actualite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()

class AdminPageStatique(admin.ModelAdmin):
    list_display = ['titre','date_creation','publie']
    prepopulated_fields = {'slug':('titre',),}
    inlines = [
        DocumentAttacheInline,
    ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = PageStatique.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()


class AdminMagazine(admin.ModelAdmin):
    list_display = ['titre','date_parution','document']
    prepopulated_fields = {'slug':('titre',),}
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = Magazine.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        
        outpoutejpg = settings.MEDIA_ROOT+'uploads/magazines/'+obj.date_parution.strftime('%y%m%d-val-d-yerres-magazine.jpg')     
        fichierpdf = settings.MEDIA_ROOT+obj.document.path
        print fichierpdf+'\r'
        print outpoutejpg+'\r'
        args = ["-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-r300",
                "-dJPEGQ=90",
                "-dFirstPage=1",
                "-dLastPage=1",
                "-sOutputFile="+outpoutejpg,
                fichierpdf ]

        ghostscript.Ghostscript(*args)
        obj.image = outpoutejpg.replace(settings.MEDIA_ROOT,"")
        
        obj.save()
    
class AdminRapportActivite(admin.ModelAdmin):
    list_display = ['titre','date_parution','document']
    prepopulated_fields = {'slug':('titre',),}
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.titre)
        if obj.slug == "":
            listsize = RapportActivite.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        fichierpdf = settings.MEDIA_ROOT+obj.document.path
        outpoutejpg = settings.MEDIA_ROOT+obj.date_parution.strftime('%y%m%d-rapport-activite.jpg')
        args = ["-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=jpeg",
                "-r300",
                "-dJPEGQ=90",
                "-dFirstPage=1",
                "-dLastPage=1",
                "-sOutputFile="+outpoutejpg,
                fichierpdf ]

        ghostscript.Ghostscript(*args)
        obj.image = outpoutejpg
        obj.save()
        
        
        
admin.site.register(Actualite, AdminActualite)     
admin.site.register(PageStatique, AdminPageStatique)
admin.site.register(Magazine, AdminMagazine)
admin.site.register(RapportActivite, AdminRapportActivite)