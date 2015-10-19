from django.contrib import admin
from models import DocumentAttacheDevEco, ActualiteDevEco, Dirigeant, Entreprise


# Register your models here.
class DocumentAttacheDevEcoInline(admin.TabularInline):
    model = DocumentAttacheDevEco
    extra = 5
    max_num = 15


class AdminActualiteDevEco(admin.ModelAdmin):
    search_fields = ['titre']
    list_display = ['titre', 'date_publication', 'publie']
    prepopulated_fields = {'slug': ('titre',), }
    fieldsets = [
        ('Page', {'fields': ['titre', 'slug', 'meta_description', 'contenu', 'image', 'publie']}),
        ('Date', {'fields': ['date_publication']}),
    ]
    inlines = [
        DocumentAttacheDevEcoInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]


class AdminEntreprise(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ['nom', 'ville', 'publie',]
    prepopulated_fields = {'slug': ('nom',), }
    fieldsets = [
        ('Entreprise', {'fields': ['nom', 'slug', 'meta_description', 'image', 'presentation', ]}),
        ('Lieu', {'fields': ['rue', 'ville', 'latitude', 'longitude']}),
        ('Internet', {'fields': ['site_internet', 'email']}),
        ('Publication', {'fields': ['publie']})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]


class AdminDirigeant(admin.ModelAdmin):
    search_fields = ['nom']
    list_display = ['nom', 'prenom', 'entreprise']
    fieldsets = [
        ('Dirigeant', {'fields': ['nom', 'prenom', 'image', 'email', 'presentation', 'entreprise']})
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


admin.site.register(ActualiteDevEco, AdminActualiteDevEco)
admin.site.register(Entreprise, AdminEntreprise)
admin.site.register(Dirigeant, AdminDirigeant)

