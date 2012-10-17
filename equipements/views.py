from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response , redirect , get_object_or_404
from equipements.models import *
from evenements.models import Evenement
from horaires.models import Horaires, Periode
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from pytz import timezone
from django.template import Context, loader
from valdyerresweb.utils.functions import GenerationQrCode
import datetime


utcTZ = timezone("UTC")

def CarteEquipements(request):
      
    equipements = Equipement.objects.select_related().all().order_by('fonction__nom', 'nom')

    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'mediaDir': settings.MEDIA_DIR_NAME})



def EquipementsDetailsHtml(request, fonction_slug, equipement_slug):

    now = datetime.datetime.now(utcTZ)
    equipement = get_object_or_404(Equipement.objects.select_related() , slug=equipement_slug)
    if fonction_slug != equipement.fonction.slug:
        raise Http404 
    
    
    qr_code_geo = GenerationQrCode("geo:" + str(equipement.latitude) + "," + str(equipement.longitude))
        
    facilites = Facilites.objects.filter(equipement_id=equipement.id)
        
    evenements = Evenement.objects.select_related().filter(lieu_id=equipement.id , fin__gt=now , publish=1).order_by('debut')
        
    qr_code_vcard = GenerationQrCode(EquipementVcard(equipement))
    #<trash>
    try:
        facilites = facilites[0]
    except:
        facilites = None
    #</trash>
        
    today = datetime.date.today()
    horaires = None
    periodes = Periode.objects.filter(date_debut__lt=today , date_fin__gt=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    if len(periodes) >= 1:
        periode_active = periodes[len(periodes) - 1]
        horaires = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active.id)
    else:
        periode_active = None
        
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    horaires_demain = None
    periodes_demain = Periode.objects.filter(date_debut__lt=tomorrow , date_fin__gt=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes_demain.query.group_by = ['periode_id']
    if len(periodes_demain) >= 1:
        periode_active_demain = periodes[len(periodes) - 1]
        horaires_demain = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id).filter(periodes__id=periode_active_demain.id)
    else:
        periode_active_demain = None
        
        
    autres_periodes = Periode.objects.filter(date_fin__gt=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    autres_periodes.query.group_by = ['periode_id']
        
    return render_to_response('equipements/equipement-details.html', {'equipement': equipement, 'qr_code_geo': qr_code_geo, 'qr_code_vcard': qr_code_vcard, 'facilites': facilites, 'evenements': evenements, 'horaires':horaires, 'periode_active':periode_active, 'autres_periodes':autres_periodes, 'horaires_demain':horaires_demain, 'periode_active_demain':periode_active_demain })


def EquipementHoraires(request, equipement_slug):
    equipement = get_object_or_404(Equipement , slug=equipement_slug)
    today = datetime.date.today()
    periodes = Periode.objects.filter(date_fin__gt=today).filter(horaires__equipement=equipement.id).order_by('date_debut')
    periodes.query.group_by = ['periode_id']
    horaires = Horaires.objects.prefetch_related('periodes').filter(equipement=equipement.id)
    for periode in periodes:
        horaires.filter(periodes__id = periode.id)
    
    if len(horaires) == 0:
        raise Http404
    
    
    return render_to_response('equipements/equipement-horaires.html', {'equipement':equipement,'horaires':horaires, 'periodes':periodes})

def FonctionDetailsHtml(request, fonction_slug):
    try:
        fonction = EquipementFonction.objects.get(slug=fonction_slug)
        equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id)
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-fonction-equipements.html', {'equipements': equipements, 'fonction': fonction})

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
