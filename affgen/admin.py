from django.contrib import admin
from models import Elu, TitreHorsAgglo, MandatAgglo

# Register your models here.

class TitreHorsAggloInline(admin.TabularInline):
    model = TitreHorsAgglo
    extra = 5
    max_num = 15

class MandatAggloInline(admin.TabularInline):
    model = MandatAgglo
    extra = 5
    max_num = 15

class LieuAdmin(admin.ModelAdmin):
    list_display = ['nom','prenom' 'ville']
    list_filter = ['nom','ville']
    search_fields = ['nom']
    inlines = [
        TitreHorsAggloInline,MandatAggloInline
    ]
