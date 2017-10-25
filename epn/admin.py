from django.contrib import admin
from .models import FicheInscription
# Register your models here.


class FicheInscriptionAdmin(admin.ModelAdmin):
    list_display= ['nom', 'prenom', 'datenaissance', 'email', 'ville']


admin.site.register(FicheInscription, FicheInscriptionAdmin)