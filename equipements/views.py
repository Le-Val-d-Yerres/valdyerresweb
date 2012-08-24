from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from equipements.models import *
from localisations.models import Lieu
from datetime import datetime
from django.db.models import Q
from django.template import Context,loader
import qrcode
import base64
import StringIO

def CarteEquipements(request):
    try:
        equipements = Equipement.objects.select_related().all()
        fonction = EquipementFonction.objects.all()
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-equipements.html', {'equipements': equipements, 'fonction': fonction})

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
        
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/equipement-details.html', {'equipement': equipement, 'qrcode': qrcode})

def FonctionDetailsHtml(request, fonction_slug):
    try:
        fonction = EquipementFonction.objects.get(slug=fonction_slug)
        equipements = Equipement.objects.select_related().filter(fonction_id=fonction.id)
    except Equipement.DoesNotExist:
        raise Http404
    return render_to_response('equipements/carte-fonction-equipements.html', {'equipements': equipements, 'fonction': fonction})
