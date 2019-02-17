# -*- coding: utf-8 -*-
from evenements.models import Evenement, Organisateur, SaisonCulturelle, TypeEvenement, Festival, Prix, DocumentAttache, \
    EvenementBib, EvenementCrd, EvenementDevEco, EvenementMde
from equipements.models import Equipement
from valdyerresweb.utils.functions import pdftojpg
from django.contrib import admin
from django.template import defaultfilters
from django import forms
from valdyerresweb import settings
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
import datetime
import os
from django.forms import FileField
from filebrowser.base import FileObject

class PrixInline(admin.TabularInline):
    model = Prix
    extra = 2
    max_num = 15


class DocumentAttacheInline(admin.TabularInline):
    model = DocumentAttache
    extra = 2
    max_num = 15


# class DateLieuEvenementInline(admin.TabularInline):
#     model = DateLieuEvenement
#     extra = 1



class EvenementAdmin(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description',
         {'fields': ['nom', 'type', 'meta_description', 'description', 'image', 'url', 'url_reservation']}),
        ('Saison Culturelle', {'fields': ['cadre_evenement', 'organisateur']}),
        ('Classification', {'fields': ['categorie', 'public']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Option de publication', {'fields': ['publish', 'complet', 'page_accueil']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish']
    filter_horizontal = ("organisateur",)

    inlines = [
        # DateLieuEvenementInline,
        PrixInline, DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):

        monslug = defaultfilters.slugify(obj.nom)

        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug__startswith=monslug).order_by('-slug')
            listsize = len(listevenement)
            if listsize > 0:
                lastslug = listevenement[0].slug
                lastslugtab = lastslug.split('-')
                lastslugindex = int(lastslugtab[len(lastslugtab) - 1])
                monslug = monslug + '-' + str(lastslugindex + 1)
            obj.slug = monslug

        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg(os.path.join(settings.MEDIA_ROOT, obj.image.path), subpath="")
                obj.image = FileObject(os.path.relpath(abspath_image, settings.MEDIA_ROOT))
        if obj.id != None:
            evenementInfo = Evenement.objects.select_related().get(slug=obj.slug)

            equipements = Equipement.objects.filter(lieu_ptr_id=evenementInfo.lieu.id)

            nbreEquipement = len(equipements)
            if nbreEquipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            equipements = Equipement.objects.filter(lieu_ptr_id=obj.lieu.id)

            nbreEquipement = len(equipements)
            if nbreEquipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            functions.resetEphemerideCache(obj.debut)

        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.cadre_evenement.slug})
        functions.expire_page(path)

        path = reverse('event-details',
                       kwargs={'slug': obj.cadre_evenement.slug, 'evenement_slug': obj.slug})
        functions.expire_page(path)


class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']
    prepopulated_fields = {'slug': ('nom',), }

    def save_model(self, request, obj, form, change):
        obj.save()
        path = reverse('agenda-type-period-orga',
                       kwargs={'type_slug': obj.slug, 'period': 'toutes', 'orga_slug': 'tous'})
        functions.expire_page(path)


class OrganisateurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'ville']
    fieldsets = [
        (None, {'fields': ['nom', 'logo', 'meta_description', 'description']}),
        ('Coordonnées', {'fields': ['url', 'email', 'telephone', 'fax', 'rue', 'ville']}),
        ('Entitées liées', {'fields': ['orga_service', 'orga_equipement', 'orga_ville']})
    ]
    list_filter = ['ville__nom']
    search_fields = ['nom']

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug=monslug)
            listsize = len(listevenement)
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
        obj.save()

        def save_model(self, request, obj, form, change):
            path = reverse('agenda-type-period-orga',
                           kwargs={'type_slug': 'tous', 'period': 'toutes', 'orga_slug': obj.slug})
            functions.expire_page(path)


class FestivalAdmin(admin.ModelAdmin):
    list_display = ['nom', 'saison_culture', 'debut', 'fin']
    fieldsets = [
        (None, {'fields': ['nom', 'description', 'saison_culture']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    list_filter = ['saison_culture__nom']
    search_fields = ['nom']

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listefestival = Festival.objects.filter(slug=monslug)
            listsize = len(listefestival)
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.slug})
        functions.expire_page(path)


class SaisonCulturelleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'debut', 'fin']
    fieldsets = [
        (None, {'fields': ['nom', 'description']}),
        ('Date', {'fields': ['debut', 'fin']}),
    ]
    search_fields = ['nom']

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',

        ]

    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.nom)
        if obj.slug == "":
            listesaisonculturelle = SaisonCulturelle.objects.filter(slug=monslug)
            listsize = len(listesaisonculturelle)
            if listsize > 0:
                monslug = monslug + '-' + str(listsize + 1)
            obj.slug = monslug
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.slug})
        functions.expire_page(path)


class BibForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BibForm, self).__init__(*args, **kwargs)
        self.fields['lieu'].queryset = Equipement.objects.filter(type="bib")


class ManageBibEvenement(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'description', 'image', 'url']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Classification', {'fields': ['public']}),
        ('Option de publication', {'fields': ['publish']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish', 'debut']

    formfield_overrides = {
        Evenement.image: {'widget': FileField},
    }

    inlines = [
        # DateLieuEvenementInline,
        PrixInline, DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    form = BibForm

    def save_model(self, request, obj, form, change):
        obj.categorie = 'bib'
        monslug = defaultfilters.slugify(obj.nom)
        userprofile = request.user.userprofile

        year = obj.debut.year
        currentmonth = obj.debut.month
        if currentmonth in [1, 2, 3, 4, 5, 6, 7, 8]:
            year = year - 1
        nomsaison = u"Bibliothèques, Médiathèques saison " + str(year) + u"-" + str(year + 1)
        slugsaison = defaultfilters.slugify(nomsaison)
        saisonculturelle = None
        try:
            saisonculturelle = SaisonCulturelle.objects.get(slug=slugsaison)
        except:
            saisonculturelle = SaisonCulturelle()
            saisonculturelle.nom = nomsaison
            saisonculturelle.slug = slugsaison
            premsept = datetime.date(year, 9, 1)
            dernaout = datetime.date(year + 1, 8, 31)
            saisonculturelle.debut = premsept
            saisonculturelle.fin = dernaout
            saisonculturelle.description = "Les évenements organisés dans les bibliothèques et médiathèques."
            saisonculturelle.save()

        obj.cadre_evenement = saisonculturelle

        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug__startswith=monslug).order_by('-slug')
            listsize = len(listevenement)
            if listsize > 0:
                lastslug = listevenement[0].slug
                lastslugtab = lastslug.split('-')
                lastslugindex = int(lastslugtab[len(lastslugtab) - 1])
                monslug = monslug + '-' + str(lastslugindex + 1)
            obj.slug = monslug


        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg(os.path.join(settings.MEDIA_ROOT, obj.image.path), subpath="")
                obj.image = FileObject(os.path.relpath(abspath_image, settings.MEDIA_ROOT))

        if obj.id != None:
            evenementinfo = Evenement.objects.select_related().get(slug=obj.slug)

            equipements = Equipement.objects.filter(lieu_ptr_id=evenementinfo.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            equipements = Equipement.objects.filter(lieu_ptr_id=obj.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            functions.resetEphemerideCache(obj.debut)

        obj.save()
        obj.organisateur.add(userprofile.organisateur)
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.cadre_evenement.slug})
        functions.expire_page(path)

        path = reverse('event-details',
                       kwargs={'slug': obj.cadre_evenement.slug, 'evenement_slug': obj.slug})
        functions.expire_page(path)


# class CrdForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CrdForm, self).__init__(*args, **kwargs)
#         self.fields['lieu'].queryset = Equipement.objects.filter(type="crd")


class ManageCrdEvenement(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'description', 'image', 'url']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Classification', {'fields': ['public']}),
        ('Option de publication', {'fields': ['publish']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish', 'debut']

    formfield_overrides = {
        Evenement.image: {'widget': FileField},
    }

    inlines = [
        # DateLieuEvenementInline,
        PrixInline, DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    #form = CrdForm

    def save_model(self, request, obj, form, change):
        obj.categorie = 'crd'
        monslug = defaultfilters.slugify(obj.nom)
        userprofile = request.user.userprofile

        year = obj.debut.year
        currentmonth = obj.debut.month
        if currentmonth in [1, 2, 3, 4, 5, 6, 7, 8]:
            year = year - 1
        nomsaison = u"Conservatoires saison " + str(year) + u"-" + str(year + 1)
        slugsaison = defaultfilters.slugify(nomsaison)
        saisonculturelle = None
        try:
            saisonculturelle = SaisonCulturelle.objects.get(slug=slugsaison)
        except:
            saisonculturelle = SaisonCulturelle()
            saisonculturelle.nom = nomsaison
            saisonculturelle.slug = slugsaison
            premsept = datetime.date(year, 9, 1)
            dernaout = datetime.date(year + 1, 8, 31)
            saisonculturelle.debut = premsept
            saisonculturelle.fin = dernaout
            saisonculturelle.description = "Les évenements organisés par les conservatoires."
            saisonculturelle.save()

        obj.cadre_evenement = saisonculturelle


        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug__startswith=monslug).order_by('-slug')
            listsize = len(listevenement)
            if listsize > 0:
                lastslug = listevenement[0].slug
                lastslugtab = lastslug.split('-')
                lastslugindex = int(lastslugtab[len(lastslugtab) - 1])
                monslug = monslug + '-' + str(lastslugindex + 1)
            obj.slug = monslug


        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg(os.path.join(settings.MEDIA_ROOT, obj.image.path), subpath="")
                obj.image = FileObject(os.path.relpath(abspath_image, settings.MEDIA_ROOT))

        if obj.id != None:
            evenementinfo = Evenement.objects.select_related().get(slug=obj.slug)

            equipements = Equipement.objects.filter(lieu_ptr_id=evenementinfo.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            equipements = Equipement.objects.filter(lieu_ptr_id=obj.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            functions.resetEphemerideCache(obj.debut)

        obj.save()
        obj.organisateur.add(userprofile.organisateur)
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.cadre_evenement.slug})
        functions.expire_page(path)

        path = reverse('event-details',
                       kwargs={'slug': obj.cadre_evenement.slug, 'evenement_slug': obj.slug})
        functions.expire_page(path)


class ManageDevEcoEvenement(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'description', 'image', 'url']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Classification', {'fields': ['public']}),
        ('Option de publication', {'fields': ['publish']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish', 'debut']

    formfield_overrides = {
        Evenement.image: {'widget': FileField},
    }

    inlines = [
        PrixInline, DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    def save_model(self, request, obj, form, change):
        obj.categorie = 'eco'
        monslug = defaultfilters.slugify(obj.nom)
        userprofile = request.user.userprofile

        year = obj.debut.year
        currentmonth = obj.debut.month
        if currentmonth in [1, 2, 3, 4, 5, 6, 7, 8]:
            year = year - 1
        nomsaison = u"Développement économique " + str(year) + u"-" + str(year + 1)
        slugsaison = defaultfilters.slugify(nomsaison)
        saisonculturelle = None
        try:
            saisonculturelle = SaisonCulturelle.objects.get(slug=slugsaison)
        except:
            saisonculturelle = SaisonCulturelle()
            saisonculturelle.nom = nomsaison
            saisonculturelle.slug = slugsaison
            premsept = datetime.date(year, 9, 1)
            dernaout = datetime.date(year + 1, 8, 31)
            saisonculturelle.debut = premsept
            saisonculturelle.fin = dernaout
            saisonculturelle.description = "Les évenements «développement économique»"
            saisonculturelle.save()

        obj.cadre_evenement = saisonculturelle

        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug__startswith=monslug).order_by('-slug')
            listsize = len(listevenement)
            if listsize > 0:
                lastslug = listevenement[0].slug
                lastslugtab = lastslug.split('-')
                lastslugindex = int(lastslugtab[len(lastslugtab) - 1])
                monslug = monslug + '-' + str(lastslugindex + 1)
            obj.slug = monslug

        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg(os.path.join(settings.MEDIA_ROOT, obj.image.path), subpath="")
                obj.image = FileObject(os.path.relpath(abspath_image, settings.MEDIA_ROOT))

        if obj.id != None:
            evenementinfo = Evenement.objects.select_related().get(slug=obj.slug)

            equipements = Equipement.objects.filter(lieu_ptr_id=evenementinfo.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            equipements = Equipement.objects.filter(lieu_ptr_id=obj.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            functions.resetEphemerideCache(obj.debut)

        obj.save()
        obj.organisateur.add(userprofile.organisateur)
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.cadre_evenement.slug})
        functions.expire_page(path)

        path = reverse('event-details',
                       kwargs={'slug': obj.cadre_evenement.slug, 'evenement_slug': obj.slug})
        functions.expire_page(path)


class ManageMdeEvenement(admin.ModelAdmin):
    list_display = ['nom', 'Organisateurs', 'lieu', 'debut', 'publish']
    fieldsets = [
        ('Description', {'fields': ['nom', 'type', 'description', 'image', 'url']}),
        ('Date et Lieu', {'fields': ['debut', 'fin', 'lieu']}),
        ('Classification', {'fields': ['public']}),
        ('Option de publication', {'fields': ['publish']}),
    ]
    search_fields = ['nom']
    list_filter = ['publish', 'debut']

    formfield_overrides = {
        Evenement.image: {'widget': FileField},
    }

    inlines = [
        PrixInline, DocumentAttacheInline,
    ]

    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

    def save_model(self, request, obj, form, change):
        obj.categorie = 'mde'
        monslug = defaultfilters.slugify(obj.nom)
        userprofile = request.user.userprofile

        year = obj.debut.year
        currentmonth = obj.debut.month
        if currentmonth in [1, 2, 3, 4, 5, 6, 7, 8]:
            year = year - 1
        nomsaison = u"Maison de l'environnement " + str(year) + u"-" + str(year + 1)
        slugsaison = defaultfilters.slugify(nomsaison)
        saisonculturelle = None
        try:
            saisonculturelle = SaisonCulturelle.objects.get(slug=slugsaison)
        except:
            saisonculturelle = SaisonCulturelle()
            saisonculturelle.nom = nomsaison
            saisonculturelle.slug = slugsaison
            premsept = datetime.date(year, 9, 1)
            dernaout = datetime.date(year + 1, 8, 31)
            saisonculturelle.debut = premsept
            saisonculturelle.fin = dernaout
            saisonculturelle.description = "Les évenements organisés par la maison de l'environnement"
            saisonculturelle.save()

        obj.cadre_evenement = saisonculturelle

        if obj.slug == "":
            listevenement = Evenement.objects.filter(slug__startswith=monslug).order_by('-slug')
            listsize = len(listevenement)
            if listsize > 0:
                lastslug = listevenement[0].slug
                lastslugtab = lastslug.split('-')
                lastslugindex = int(lastslugtab[len(lastslugtab) - 1])
                monslug = monslug + '-' + str(lastslugindex + 1)
            obj.slug = monslug

        if obj.image != "":
            pouet, imageextension = os.path.splitext(obj.image.path)
            imageextension = imageextension.lower()
            if imageextension == ".pdf":
                abspath_image = pdftojpg(os.path.join(settings.MEDIA_ROOT, obj.image.path), subpath="")
                obj.image = FileObject(os.path.relpath(abspath_image, settings.MEDIA_ROOT))

        if obj.id != None:
            evenementinfo = Evenement.objects.select_related().get(slug=obj.slug)

            equipements = Equipement.objects.filter(lieu_ptr_id=evenementinfo.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            equipements = Equipement.objects.filter(lieu_ptr_id=obj.lieu.id)

            nbrequipement = len(equipements)
            if nbrequipement > 0:
                for equipement in equipements:
                    path = reverse('equipement-details',
                                   kwargs={'fonction_slug': equipement.fonction.slug,
                                           'equipement_slug': equipement.slug})
                    functions.expire_page(path)

            functions.resetEphemerideCache(obj.debut)

        obj.save()
        obj.organisateur.add(userprofile.organisateur)
        obj.save()

        path = reverse('saison-details', kwargs={'slug': obj.cadre_evenement.slug})
        functions.expire_page(path)

        path = reverse('event-details',
                       kwargs={'slug': obj.cadre_evenement.slug, 'evenement_slug': obj.slug})
        functions.expire_page(path)


admin.site.register(Evenement, EvenementAdmin)
admin.site.register(EvenementBib, ManageBibEvenement)
admin.site.register(EvenementCrd, ManageCrdEvenement)
admin.site.register(EvenementDevEco, ManageDevEcoEvenement)
admin.site.register(EvenementMde, ManageMdeEvenement)
admin.site.register(Organisateur, OrganisateurAdmin)
admin.site.register(SaisonCulturelle, SaisonCulturelleAdmin)
admin.site.register(TypeEvenement, TypeEvenementAdmin)
admin.site.register(Festival, FestivalAdmin)
