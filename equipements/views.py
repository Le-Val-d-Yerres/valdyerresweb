from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from equipements.models import *
from evenements.models import Evenement
from datetime import datetime
from django.db.models import Q
from django.conf import settings
import qrcode
import base64
import StringIO

def CarteEquipements(request):
    try:
        equipements = Equipement.objects.select_related().all()
        fonction = EquipementFonction.objects.all()
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'fonction': fonction, 'mediaDir': settings.MEDIA_DIR_NAME})

def GenerationQrCode(data):
    img_io = StringIO.StringIO()
    qr = qrcode.QRCode(
                          error_correction=qrcode.constants.ERROR_CORRECT_L,
                          box_size=3,
                          border=1,
                          )
    qr.add_data(data);
    imgQr = qr.make_image()
    imgQr.save(img_io,'PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue())

def EquipementsDetailsHtml(request, fonction_slug, equipement_slug):
    try:
        equipement = Equipement.objects.select_related().get(slug=equipement_slug)
        
        qrcode = GenerationQrCode("geo:"+str(equipement.latitude)+","+str(equipement.longitude))
        
        facilites = Facilites.objects.filter(equipement_id=equipement.id)
        
        Evenements = equipement.lieu_evenements.select_related().filter(fin__gt=datetime.now())
        #<trash>
        try:
            facilites = facilites[0]
        except:
            facilites = None
        #</trash>
        
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/equipement-details.html', {'equipement': equipement, 'qrcode': qrcode, 'facilites': facilites, 'Evenements': Evenements})

def FonctionDetailsHtml(request, fonction_slug):
    try:
        fonction = EquipementFonction.objects.get(slug=fonction_slug)
        equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id)
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-fonction-equipements.html', {'equipements': equipements, 'fonction': fonction})
