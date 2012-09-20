from menu.models import MenuItem
from django.contrib import admin
from django.template import defaultfilters

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['nom','chemin','description','index','parent']
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
        
        
admin.site.register(MenuItem, MenuItemAdmin)