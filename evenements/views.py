from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from evenements.models import *
from localisations.models import Lieu
from datetime import datetime
from django.db.models import Q
from django.template import Context,loader
import qrcode
import base64
import StringIO

def Agenda(request):
    try:
        liste_saisons = Saison.objects.filter(fin__gt=datetime.now())
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda.html', {'liste_evenement': liste_saisons})

def SaisonDetailsHtml(request, saison_slug):
    try:
        saison = Saison.objects.get(slug=saison_slug)
        festival = Festival.objects.filter(saison_culture_id=saison.id)
        evenements = Evenement.objects.select_related(depth=1).filter(fin__gt=datetime.now()).filter(publish=1)
        
        filtre = Q(cadre_evenement_id=saison.id)
        for each in festival:
            filtre.add(Q(cadre_evenement_id=each.id), 'OR')
            
        liste_evenement = evenements.order_by('-haut_page').filter(filtre)
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/saison-details.html', {'liste_evenement': liste_evenement, 'saison': saison})

def EvenementDetailsIcalendar(evenement):
    myTemplate = loader.get_template('evenements/evenement-details.ics.html')
    myContext = Context({"evenement": evenement})
    return myTemplate.render(myContext)
    
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

def SaisonEvenementDetailsHtml(request, saison_slug, evenement_slug, festival_slug = None):
    try:
        saison = Saison.objects.get(slug=saison_slug)
        evenement = Evenement.objects.select_related(depth=1).get(slug=evenement_slug)
        tarifs = Tarification.objects.filter(evenement_id=evenement.id)
        
        evenement_qr = GenerationQrCode(EvenementDetailsIcalendar(evenement))
        
        localisation_qr = list()
        for each in evenement.lieu.all():
            localisation_qr.append(GenerationQrCode("geo:"+str(each.latitude)+","+str(each.longitude)))

        #<trash>
        try:
            tarifs = tarifs[0]
        except:
            tarifs = None
        #</trash>
        
            
        if festival_slug != None:
            festival = Festival.objects.get(slug=festival_slug)
        else:
            festival = None   
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/evenement-details.html', {'evenement': evenement, 'saison': saison, 'festival': festival, 'tarifs': tarifs, 'evenement_qr': evenement_qr, 'localisation_qr': localisation_qr })



def SaisonEvenementDetailsICS(request, saison_slug, evenement_slug, festival_slug = None):
    try:
        evenement = Evenement.objects.select_related(depth=1).get(slug=evenement_slug)
        myText = EvenementDetailsIcalendar(evenement)
    except Evenement.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")
    #return render_to_response('evenements/evenement-details.ics.html', {'evenement': evenement})


def SaisonFestivalDetailsHtml(request, saison_slug, festival_slug):
    try:
        saison = SaisonCulturelle.objects.get(slug=saison_slug)
        details_festival = Festival.objects.get(slug=festival_slug)
        liste_evenement = Evenement.objects.filter(cadre_evenement_id=details_festival.id)
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/festival-details.html', {'liste_evenement': liste_evenement, 'details_festival' : details_festival, 'saison' : saison})