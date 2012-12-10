from cinemas.models import Cinema,Film,Seance 
from django.contrib import admin
from django.template import defaultfilters
from localisations.models import Lieu


class SeanceInline(admin.TabularInline):
    model = Seance
    

class CinemaAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ville','id_allocine_cine']
    fieldsets = [
        ('Description', {'fields': (('nom'), 'image')}),
        ('Adresse', {'fields': ['rue', 'ville', 'latitude', 'longitude']}),
        ('Contact', {'fields': ['telephone', 'fax', 'email']}),
        ('Allocine',{'fields': ['id_allocine_cine']}),
    ]
    
class FilmAdmin(admin.ModelAdmin):
    list_display = ['titre']
    fields = ('titre','id_allocine_film','duree','url_allocine_image','image')
    inlines = [
        SeanceInline,
    ]
    
    
admin.site.register(Cinema,CinemaAdmin)
admin.site.register(Film,FilmAdmin)