from annoncesemploi.models import Annonce ,ImportGIDEM
from django.contrib import admin
from django.template import defaultfilters
from accounts.models import UserProfile
import xlrd


class AnnonceAdmin(admin.ModelAdmin):
    list_display = [ 'intitule', 'service', 'publie']
    search_fields = ['intitule']
    list_filter = ['publié']
    
    fieldsets = [('Service et publication', {'fields': ['service', 'publie']}),
                 ('Contenu', {'fields': ['intitule','description', 'formation','experience_requise','nom_employeur','lieu_travail','contact']}),
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
    
class ImportGIDEMAdmin():
    list_display = ['id','date_import']
    search_fields = ['date_import']
    list_filter = ['date_import']
    fieldsets = [('Import GIDEM', {'fields': ['fichier_xls']}),]
    
    def save_model(self, request, obj, form, change):
        user_profile = request.user.get_profile()
        id_service = user_profile.service.id
        to_delete = Annonce.objects.filter(service=id_service)
        to_delete.delete()
        workbook = xlrd.open_workbook(obj.filename)
        worksheet = workbook.sheet_by_index(0)
        annonce = Annonce()
        
        for row in range(1,worksheet.nrows):
            annonce.service = id_service
            annonce.intitule = worksheet.cell(row,2).value.lower().capitalize()
            annonce.slug =  defaultfilters.slugify(annonce.intitule+"-"+str(obj.id))
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
            annonce.save()
            
        
        
        
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(ImportGIDEM,ImportGIDEMAdmin)        
