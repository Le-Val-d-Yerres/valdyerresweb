from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from equipements.models import *
from evenements.models import Evenement
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from pytz import timezone
from django.template import Context,loader
from valdyerresweb.utils.functions import GenerationQrCode

def CarteEquipements(request):
    try:
        equipements = Equipement.objects.select_related().all()
        fonction = EquipementFonction.objects.all()
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'fonction': fonction, 'mediaDir': settings.MEDIA_DIR_NAME})



def EquipementsDetailsHtml(request, fonction_slug, equipement_slug):
    try:
        equipement = Equipement.objects.select_related().get(slug=equipement_slug)
        
        qr_code_geo = GenerationQrCode("geo:"+str(equipement.latitude)+","+str(equipement.longitude))
        
        facilites = Facilites.objects.filter(equipement_id=equipement.id)
        
        evenements = Evenement.objects.select_related().filter(lieu_id=equipement.id).filter(publish=1).order_by('debut')
        
        qr_code_vcard = GenerationQrCode(EquipementVcard(equipement))
        #<trash>
        try:
            facilites = facilites[0]
        except:
            facilites = None
        #</trash>
        
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/equipement-details.html', {'equipement': equipement, 'qr_code_geo': qr_code_geo, 'qr_code_vcard': qr_code_vcard, 'facilites': facilites, 'Evenements': evenements})

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
    return HttpResponse(myText,content_type="text/vcard")

def EquipementVcard(equipement):
    myTemplate = loader.get_template('equipements/equipement.vcf.html')
    myContext = Context({"equipement": equipement, "settings": settings})
    return myTemplate.render(myContext)
