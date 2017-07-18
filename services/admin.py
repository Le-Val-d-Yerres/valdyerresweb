# -*- coding: utf-8 -*-

from django.contrib import admin
from django.template import defaultfilters
from services.models import Service,PageStatiqueService,DocumentAttache
from equipements.models import EquipementFonction,Equipement
from django.utils.timezone import utc
import datetime
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse


class AdminService(admin.ModelAdmin):
    list_display = ['nom', 'index', 'parent']
    prepopulated_fields = {'slug':('nom',),}
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]
        
    def save_model(self, request, obj, form, change):
        path = reverse('services', kwargs={})
        functions.expire_page(path)
        
        typesEquipement = EquipementFonction.objects.filter(service = obj.id)
        
        for fonction in typesEquipement:
            Equipements = Equipement.objects.filter(fonction = fonction.id)
            
            for equipement in Equipements:
                path = reverse('equipement-details', kwargs={'fonction_slug':fonction.slug,'equipement_slug':equipement.slug})
                functions.expire_page(path)
        
        obj.save()
      
class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 1
    
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

class AdminPageStatiqueService(admin.ModelAdmin):
    list_display=['titre','service','index','publie']
    prepopulated_fields = {'slug':('titre',),}
    
    inlines = [
        DocumentAttacheInline,
    ]
    
    def save_model(self, request, obj, form, change):
        path = reverse('page-contenu', kwargs={'service_slug':obj.service.slug,'page_slug':obj.slug})
        functions.expire_page(path)
        
        obj.save()

admin.site.register(Service, AdminService)
admin.site.register(PageStatiqueService, AdminPageStatiqueService)
