from django.contrib import admin
from models import Disciplinestagecrd, Stage, Fichestagecrd, Intitulestage


class StageInline(admin.TabularInline):
    model = Stage
    extra = 0



class FicheStageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom']
    search_fields = ['nom']
    inlines = [StageInline]


class DisciplinestagecrdAdmin(admin.ModelAdmin):
    list_display = ['nom', 'index']

class IntitulestageAdmin(admin.ModelAdmin):
    list_display = ['nom', 'duree', 'index']


admin.site.register(Disciplinestagecrd, DisciplinestagecrdAdmin)
admin.site.register(Stage)
admin.site.register(Fichestagecrd,FicheStageAdmin)
admin.site.register(Intitulestage, IntitulestageAdmin)