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
        ('Contact', {'fields': ['telephone', 'fax', 'email', 'url']}),
        ('Allocine',{'fields': ['id_allocine_cine']}),
    ]
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listelieu = Lieu.objects.filter(slug=monslug)
            listsize = len(listelieu)
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
    
class FilmAdmin(admin.ModelAdmin):
    list_display = ['titre']
    fields = ('titre','id_allocine_film','duree','url_allocine_image','image')
    
    
class SeanceAdmin(admin.ModelAdmin):
    list_display = ['film','cinema','date_debut','format','version_lang']
    fields = ('film','cinema','id_allocine_film','date_debut','date_fin','format','version_lang','version_vo')


admin.site.register(Cinema,CinemaAdmin)
admin.site.register(Film,FilmAdmin)
admin.site.register(Seance,SeanceAdmin)