# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from django.template import defaultfilters
from aide.models import Aide

class AideAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}

    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
        
admin.site.register(Aide, AideAdmin)
