from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response , redirect , get_object_or_404, get_list_or_404
from equipements.models import Equipement,EquipementFonction,TarifCategorie,Tarif , Facilites,Facilite
from evenements.models import Evenement, Organisateur
from localisations.models import Lieu
from horaires.models import Horaires, Periode
import datetime
from django.db.models import Q
from django.conf import settings
from pytz import timezone
from django.template import Context, loader
from valdyerresweb.utils.functions import GenerationQrCode
from django.views.decorators.cache import cache_control, cache_page


utcTZ = timezone("UTC")

def CarteEquipements(request):
      
    equipements = Equipement.objects.select_related().all().order_by('fonction__nom', 'ville__nom')

    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'mediaDir': settings.MEDIA_DIR_NAME})

def CarteFacilite(request,slug):
    
    facilite = get_object_or_404(Facilite.objects.filter(slug=slug))
    facilites = Facilites.objects.select_related().prefetch_related().filter(facilites=facilite.id)
    return render_to_response('equipements/carte-facilites.html', {'facilite': facilite,'facilites': facilites, 'mediaDir': settings.MEDIA_DIR_NAME})

@cache_control(must_revalidate=True, max_age=3600)
@cache_page(3600)
def EquipementsDetailsHtml(request, fonction_slug, equipement_slug):

    now = datetime.datetime.now(utcTZ)
    equipement = get_object_or_404(Equipement.objects.select_related(), slug=equipement_slug)
     
    tarif_categorie_principale = TarifCategorie.objects.select_related().filter(equipement_fonction = equipement.fonction,index=0 ) 
    tarifs_principaux = Tarif.objects.select_related().filter(categorie= tarif_categorie_principale )
        
    facilites = Facilites.objects.filter(equipement_id=equipement.id)
    
    evenements = None
    try:
        organisateur = Organisateur.objects.get(orga_equipement = equipement.id)
        evenements = Evenement.objects.select_related().filter(Q(organisateur = organisateur.id) | Q(lieu_id=equipement.id) , fin__gt=now , publish=True).order_by('debut')
    except Organisateur.DoesNotExist:
        evenements = Evenement.objects.select_related().filter(lieu_id=equipement.id , fin__gt=now , publish=True).order_by('debut')
        
    
    #<trash>
    try:
        facilites = facilites[0]
    except:
        facilites = None
    #</trash>
        
    today = datetime.date.today()
    horaires = None
    periodes = Periode.objects.filter(date_debut__lte=today , date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    if len(periodes) >= 1:
        periode_active = periodes[len(periodes) - 1]
        horaires = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active.id)
    else:
        periode_active = None
        
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    horaires_demain = None
    periodes_demain = Periode.objects.filter(date_debut__lte=tomorrow , date_fin__gte=tomorrow).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes_demain.query.group_by = ['periode_id']
    if len(periodes_demain) >= 1:
        periode_active_demain = periodes[len(periodes) - 1]
        horaires_demain = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active_demain.id)
    else:
        periode_active_demain = None
        
        
    autres_periodes = Periode.objects.filter(date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    autres_periodes.query.group_by = ['periode_id']
    
    horaires_plus_7 = list()
    
    for index in range(1,8):
        day = datetime.date.today() + datetime.timedelta(days=index)
        horaires_jour = None
        periodes_jour = Periode.objects.filter(date_debut__lte=day , date_fin__gte=day).filter(horaires__equipement=equipement.id).order_by('date_debut')
        periodes_jour.query.group_by = ['periode_id']
        if len(periodes_jour) >= 1:
            periode_active_jour = periodes_jour[len(periodes_jour) - 1]
            horaires_jour = Horaires.objects.filter(equipement=equipement.id).filter(periodes__id=periode_active_jour.id)
            horaires_plus_7.append(horaires_jour)
        else:
            periode_active_jour = None
         
    qr_code_geo = GenerationQrCode("geo:" + str(equipement.latitude) + "," + str(equipement.longitude))
    qr_code_vcard = GenerationQrCode(EquipementVcard(equipement))
        
    return render_to_response('equipements/equipement-details.html', {'equipement': equipement, 'qr_code_geo': qr_code_geo, 'qr_code_vcard': qr_code_vcard, 'facilites': facilites, 'evenements': evenements, 'horaires':horaires, 'periode_active':periode_active, 'autres_periodes':autres_periodes, 'horaires_demain':horaires_demain, 'periode_active_demain':periode_active_demain , 'horaires_plus_7': horaires_plus_7, 'tarifs_principaux':tarifs_principaux })

def EquipementHoraires(request, equipement_slug):
    equipement = get_object_or_404(Equipement.objects.select_related() , slug=equipement_slug)
    today = datetime.date.today()
    periodes = Periode.objects.filter(date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    horaires = Horaires.objects.prefetch_related('periodes').select_related().filter(equipement=equipement.id)
    for periode in periodes:
        horaires.filter(periodes__id = periode.id)
    
    if len(horaires) == 0:
        raise Http404
    
    
    return render_to_response('equipements/equipement-horaires.html', {'equipement':equipement,'horaires':horaires, 'periodes':periodes})


def EquipementFonctionTarifs(request, equipement_fonction_slug):
    tarifs = Tarif.objects.select_related().filter(categorie__equipement_fonction__slug = equipement_fonction_slug)
    fonction = EquipementFonction.objects.get(slug=equipement_fonction_slug)
    equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id).order_by('ville__nom')
            
    return render_to_response('equipements/equipement-tarifs.html', {'tarifs':tarifs,'equipements':equipements})
    


def FonctionDetailsHtml(request, fonction_slug):
    try:
        fonction = EquipementFonction.objects.get(slug=fonction_slug)
        equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id).order_by('ville__nom')
            
        today = datetime.date.today()
        listhoraires = list()
        
        for equipement in equipements:
            periodes = Periode.objects.filter(date_debut__lte=today , date_fin__gte=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
            if len(periodes) >= 1:
                periodes.query.group_by = ['periode_id']
                periode_active = periodes[len(periodes) - 1]
                horaires = Horaires.objects.select_related().filter(equipement=equipement.id).filter(periodes__id=periode_active.id)
                listhoraires.append(horaires)
            
        
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-fonction-equipements.html', {'equipements': equipements, 'fonction': fonction, 'listhoraires': listhoraires})

def EquipementVCF(request, slug):
    try:
        lieu = Lieu.objects.select_related().select_subclasses().get(slug=slug)
        
        myText = EquipementVcard(lieu)
    except Lieu.DoesNotExist:
        raise Http404
    return HttpResponse(myText, content_type="text/vcard")

def EquipementVcard(equipement):
    myTemplate = loader.get_template('equipements/equipement.vcf.html')
    myContext = Context({"equipement": equipement, "settings": settings})
    return myTemplate.render(myContext)
