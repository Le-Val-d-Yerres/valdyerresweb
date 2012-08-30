from horaires.models import Horaires, HorairesVacances, Vacances

from django.contrib import admin
from django.template import defaultfilters

class HorairesAdmin(admin.ModelAdmin):
    
    fieldsets= (
                ("Infos", 
                    { 'fields' : ('nom','equipement')
                     
                     }
                 ),
                ("Lundi",
                  { 'fields' : ('lundi_matin_debut','lundi_matin_fin')
                   }),
                 
                 )


admin.site.register(Horaires, HorairesAdmin)