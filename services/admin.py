# -*- coding: utf-8 -*-

from django.contrib import admin
from django.template import defaultfilters
from services.models import Service,PageStatiqueService,DocumentAttache


class AdminService(admin.ModelAdmin):
    list_display = ['nom', 'index', 'parent']
    prepopulated_fields = {'slug':('nom',),}
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
      
class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 1
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]

class AdminPageStatiqueService(admin.ModelAdmin):
    list_display=['titre','service','index','publie']
    prepopulated_fields = {'slug':('titre',),}
    
    inlines = [
        DocumentAttacheInline,
    ]

admin.site.register(Service, AdminService)
admin.site.register(PageStatiqueService, AdminPageStatiqueService)
