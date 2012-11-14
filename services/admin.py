# -*- coding: utf-8 -*-

from django.contrib import admin
from django.template import defaultfilters
from services.models import Service,PageStatiqueService,DocumentAttache


class AdminService(admin.ModelAdmin):
    list_display = ['nom', 'index', 'parent']
      
class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 5
    max_num = 15  

class AdminPageStatiqueService(admin.ModelAdmin):
    list_display=['titre','service','index','publie']
    prepopulated_fields = {'slug':('titre',),}
    
    inlines = [
        DocumentAttacheInline,
    ]

admin.site.register(Service, AdminService)
admin.site.register(PageStatiqueService, AdminPageStatiqueService)
