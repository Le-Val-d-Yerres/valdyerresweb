# -*- coding: utf-8 -*-

from menu.models import MenuItem
from django.contrib import admin
from django.template import defaultfilters
from django.core.cache import cache

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['nom','chemin','index','parent']
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        obj.save()
        print "clear cache"
        cache.clear()
        
admin.site.register(MenuItem, MenuItemAdmin)