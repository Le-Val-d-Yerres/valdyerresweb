from django.contrib import admin
from django.template import defaultfilters
from services.models import Service,PageStatiqueService


class AdminService(admin.ModelAdmin):
    list_display = ['nom', 'index', 'parent']
        

class AdminPageStatiqueService(admin.ModelAdmin):
    list_display=['titre','service','index','publie']

admin.site.register(Service, AdminService)

