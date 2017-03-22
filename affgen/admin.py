# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Elu, TitreHorsAgglo, MandatAgglo, QualifMandat

# Register your models here.

class TitreHorsAggloInline(admin.TabularInline):
    model = TitreHorsAgglo
    extra = 1
    max_num = 15

class MandatAggloInline(admin.TabularInline):
    model = MandatAgglo
    extra = 1
    max_num = 15

class QualifMandatAdmin(admin.ModelAdmin):
    list_display = ['nom', 'index']

class EluAdmin(admin.ModelAdmin):

    def titres(self):
        html = ''
        for obj in TitreHorsAgglo.objects.filter(elu__id = self.id):
            html += "<p>%s</p>"%obj.nom
        return html

    def mandats(self):
        html = ''
        for obj in MandatAgglo.objects.filter(elu__id=self.id):
            html += "<p>%s</p>" % obj.nom
        return html

    titres.allow_tags = True
    mandats.allow_tags = True
    list_display = ['nom', 'prenom', 'sexe', 'ville',titres,mandats,'publie']
    list_filter = ['ville', 'sexe','publie']
    search_fields = ['nom']
    inlines = [
        TitreHorsAggloInline,MandatAggloInline
    ]


admin.site.register(Elu,EluAdmin)
admin.site.register(QualifMandat,QualifMandatAdmin)
