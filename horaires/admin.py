from horaires.models import Horaires, Periode

from django.contrib import admin


class HorairesAdmin(admin.ModelAdmin):
    
    fieldsets= (
                ("Infos", 
                    { 'fields' : ('nom','equipement','periodes', )
                     
                     }
                 ),
                ("Lundi",
                  { 'fields' : (('lundi_matin_debut','lundi_matin_fin','lundi_matin_ferme'),('lundi_am_debut','lundi_am_fin','lundi_am_ferme'),'lundi_journee_continue')
                   }),
                 ("Mardi",
                  { 'fields' : (('mardi_matin_debut','mardi_matin_fin','mardi_matin_ferme'),('mardi_am_debut','mardi_am_fin','mardi_am_ferme'),'mardi_journee_continue')
                   }),
                ("Mercredi",
                  { 'fields' : (('mercredi_matin_debut','mercredi_matin_fin','mercredi_matin_ferme'),('mercredi_am_debut','mercredi_am_fin','mercredi_am_ferme'),'mercredi_journee_continue')
                   }),
                ("Jeudi",
                  { 'fields' : (('jeudi_matin_debut','jeudi_matin_fin','jeudi_matin_ferme'),('jeudi_am_debut','jeudi_am_fin','jeudi_am_ferme'),'jeudi_journee_continue')
                   }),
                ("Vendredi",
                  { 'fields' : (('vendredi_matin_debut','vendredi_matin_fin','vendredi_matin_ferme'),('vendredi_am_debut','vendredi_am_fin','vendredi_am_ferme'),'vendredi_journee_continue')
                   }),
                ("Samedi",
                  { 'fields' : (('samedi_matin_debut','samedi_matin_fin','samedi_matin_ferme'),('samedi_am_debut','samedi_am_fin','samedi_am_ferme'),'samedi_journee_continue')
                   }),
                ("Dimanche",
                  { 'fields' : (('dimanche_matin_debut','dimanche_matin_fin','dimanche_matin_ferme'),('dimanche_am_debut','dimanche_am_fin','dimanche_am_ferme'),'dimanche_journee_continue')
                   }),
                 )
    filter_horizontal = ("periodes",)
    
    
    class Media:
        js = (
            'admin/js/admin/horaires_admin.js',
        )
        
class PeriodeAdmin(admin.ModelAdmin):
    list_display = ('nom','date_debut','date_fin')
    
    


admin.site.register(Horaires, HorairesAdmin)
admin.site.register(Periode, PeriodeAdmin)
