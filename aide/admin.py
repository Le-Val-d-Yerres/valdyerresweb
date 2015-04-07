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
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]
        
admin.site.register(Aide, AideAdmin)
