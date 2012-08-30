from horaires.models import Horaires, HorairesVacances, Vacances

from django.contrib import admin
from django.template import defaultfilters

class HorairesAdmin(admin.ModelAdmin):
    
    fieldsets= (
                ("Infos", 
                    { 'fields' : ('nom','equipement','date_debut','date_fin')
                     
                     }
                 ),
                ("Lundi",
                  { 'fields' : ('lundi_matin_debut','lundi_matin_fin','lundi_am_debut','lundi_am_fin','lundi_journee_continue')
                   }),
                 ("Mardi",
                  { 'fields' : ('mardi_matin_debut','mardi_matin_fin','mardi_am_debut','mardi_am_fin','mardi_journee_continue')
                   }),
                 )


admin.site.register(Horaires, HorairesAdmin)