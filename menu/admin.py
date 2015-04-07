# -*- coding: utf-8 -*-

from menu.models import MenuItem
from django.contrib import admin
from django.template import defaultfilters

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['nom','chemin','index','parent']
    
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]
    
    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(MenuItem, MenuItemAdmin)