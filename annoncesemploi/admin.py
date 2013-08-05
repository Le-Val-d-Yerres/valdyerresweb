# -*- coding: utf-8 -*-

from annoncesemploi.models import Annonce ,ImportGIDEM
from django.contrib import admin
from django.template import defaultfilters
from accounts.models import UserProfile
from services.models import Service
from valdyerresweb import settings
from valdyerresweb.utils import functions
from django.core.urlresolvers import reverse
import xlrd
import datetime , os


class AnnonceAdmin(admin.ModelAdmin):
    list_display = [ 'intitule', 'service', 'publie']
    search_fields = ['intitule']
    list_filter = ['publie']
    
    fieldsets = [('Service et publication', {'fields': ['service', 'publie']}),
                 ('Contenu', {'fields': ['intitule','description_du_poste', 'niveau_formation','experience_requise','nom_employeur','lieu_travail','contact']}),
                 ('Contenu additionnel GIDEM', {'fields': ['type_de_poste','secteur_activite','salaire_indicatif','nb_postes','deplacement']}),
                 ]
    
    class Media:
        js = [
            'js/tinymce/tiny_mce.js',
            'js/tinymce/tinymce_setup.js',
            'filebrowser/js/TinyMCEAdmin.js',
        ]
    
    def save_model(self, request, obj, form, change):
        monslug = defaultfilters.slugify(obj.intitule)
        if obj.slug == "":
            listsize = Annonce.objects.filter(slug=monslug).count()
            if listsize > 0:
                monslug = monslug+'-'+str(listsize+1)
            obj.slug = monslug
        obj.save()
        
        path = reverse('annoncesemploi.views.AnnonceDetail', kwargs={'annonce_slug':obj.slug,'service_slug':obj.service.slug})
        functions.expire_page(path)
        
        path = reverse('annoncesemploi.views.AnnoncesList', kwargs={})
        functions.expire_page(path)
        
        path = reverse('annoncesemploi.views.AnnoncesListService', kwargs={'service_slug':obj.service.slug})
        functions.expire_page(path)
    
class ImportGIDEMAdmin(admin.ModelAdmin):
    list_display = ['id','date_import']
    search_fields = ['date_import']
    list_filter = ['date_import']
    fieldsets = [('Import GIDEM', {'fields': ['fichier_xls']}),]
    
    def save_model(self, request, obj, form, change):
        obj.date_import = datetime.datetime.utcnow()
        obj.save()
        
        user_profile = request.user.get_profile()
        id_service = user_profile.service.id
        to_delete = Annonce.objects.filter(service=id_service)
        
        to_delete.delete()
        workbook = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT,obj.fichier_xls.name))
        worksheet = workbook.sheet_by_index(0)
        
        myservice = Service.objects.get(id=id_service)
        
        loop = 1
        
        for row in range(1,worksheet.nrows):
            annonce = Annonce()
            annonce.service = myservice
            annonce.intitule = worksheet.cell(row,2).value.lower().capitalize()
            annonce.slug =  defaultfilters.slugify(annonce.intitule+"-"+str(loop))
            annonce.type_de_poste = worksheet.cell(row,7).value
            annonce.secteur_activite = worksheet.cell(row,4).value
            annonce.niveau_formation = worksheet.cell(row,10).value
            annonce.experience_requise = worksheet.cell(row,9).value
            annonce.description_du_poste = worksheet.cell(row,8).value
            annonce.nom_employeur = worksheet.cell(row,5).value
            annonce.contact = worksheet.cell(row,6).value
            annonce.nbpostes = worksheet.cell(row,11).value
            annonce.deplacement = worksheet.cell(row,15).value
            annonce.lieu_travail = worksheet.cell(row,12).value 
            annonce.salaire_indicatif = worksheet.cell(row,14).value
            try :
                annonce.salaire_indicatif = float(annonce.salaire_indicatif)
            except:
                annonce.salaire_indicatif = ""
            
            if annonce.salaire_indicatif == 0.0:
                annonce.salaire_indicatif = ""
            annonce.publie = True
            annonce.save()
            loop = loop+1
            
            path = reverse('annoncesemploi.views.AnnonceDetail', kwargs={'annonce_slug':annonce.slug,'service_slug':annonce.service.slug})
            functions.expire_page(path)
            
            path = reverse('annoncesemploi.views.AnnoncesList', kwargs={})
            functions.expire_page(path)
            
            path = reverse('annoncesemploi.views.AnnoncesListService', kwargs={'service_slug':annonce.service.slug})
            functions.expire_page(path)
            
        
        
        
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(ImportGIDEM,ImportGIDEMAdmin)        
