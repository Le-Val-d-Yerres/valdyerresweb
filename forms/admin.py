from django.contrib import admin
from models import Disciplinestagecrd, Stage, Fichestagecrd, Intitulestage


class StageInline(admin.TabularInline):
    model = Stage



class FicheStageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom']
    search_fields = ['nom']

    inlines = [StageInline]

admin.site.register(Disciplinestagecrd)
admin.site.register(Stage)
admin.site.register(Fichestagecrd,FicheStageAdmin)
admin.site.register(Intitulestage)