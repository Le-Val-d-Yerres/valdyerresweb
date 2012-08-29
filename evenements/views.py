from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from evenements.models import *
from localisations.models import Lieu
import datetime
from django.db.models import Q
from django.template import Context,loader
from evenements.customCalendar.calendrier import CAVYCalendar, entierAvecZero
import qrcode
import base64
import StringIO
import calendar
from equipements.models import Equipement
from pytz import tzinfo,timezone
from valdyerresweb import settings

utcTZ = timezone("UTC")
        
def AgendaMois(request, annee, mois):
    try:
        month = int(mois)
        year = int(annee)
    
        if month == 1:
            mois_prec = '12'
            annee_prec = str(year-1)
        else:
            annee_prec = str(year)
            mois_prec = entierAvecZero(month-1)
            

        if month == 12:
            mois_suiv = '01'
            annee_suiv = str(year+1)
        else:
            mois_suiv = entierAvecZero(month+1)
            annee_suiv = str(year)
    
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.datetime(year, month, dayStart,0,0,0,tzinfo=utcTZ)
        DateFin = datetime.date(year, month, dayEnd)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        evenements = list()
        
        saisons = SaisonCulturelle.objects.filter(fin__gt=datetime.datetime.now())
        listeFestival = list()
        
        for each in saisons:
            festivals = Festival.objects.select_related().filter(saison_culture_id=each.id)
            for eachFestival in festivals:
                listeFestival.append(eachFestival)
            
        for each in liste_event:
            evenements.append(each)
            
        CAVYcalendrier = CAVYCalendar(evenements, listeFestival)

        calendrier = CAVYcalendrier.formatmonth(year, month)
    except Saison.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv})

def AgendaAnnee(request, annee):
    try:
        year = int(annee)
        
        DateDebut = datetime.date(year, 1, 31)
        DateFin = datetime.date(year, 12, 31)
        liste_evenements = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda-annee.html', {'liste_evenement': liste_evenements, 'annee': annee})

def AgendaNow(request):
    try:
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        
        if month == 1:
            mois_prec = '12'
            annee_prec = str(year-1)
        else:
            annee_prec = str(year)
            mois_prec = entierAvecZero(month-1)
            

        if month == 12:
            mois_suiv = '01'
            annee_suiv = str(year+1)
        else:
            mois_suiv = entierAvecZero(month+1)
            annee_suiv = str(year)
        
        dayEnd = calendar.monthrange(year, month)[1]
        dayStart = 1
        
        DateDebut = datetime.date(year, month, dayStart)
        DateFin = datetime.date(year, month, dayEnd)
        
        liste_event = Evenement.objects.select_related().filter(debut__gt=DateDebut).filter(fin__lt=DateFin)
        evenements = list()
        
        saisons = SaisonCulturelle.objects.filter(fin__gt=datetime.datetime.now())
        listeFestival = list()
        
        for each in saisons:
            festivals = Festival.objects.select_related().filter(saison_culture_id=each.id)
            for eachFestival in festivals:
                listeFestival.append(eachFestival)
            
        for each in liste_event:
            evenements.append(each)
        
        CAVYcalendrier = CAVYCalendar(evenements, listeFestival)
        calendrier = CAVYcalendrier.formatmonth(year, month)
    except Saison.DoesNotExist:
        raise Http404
    return render_to_response('evenements/agenda.html', {'calendrier': calendrier, 'annee_prec': annee_prec, 'mois_prec': mois_prec, 'annee_suiv': annee_suiv, 'mois_suiv': mois_suiv})

def SaisonDetailsHtml(request, slug):
    try:
        saison = Saison.objects.select_related().select_subclasses().get(slug=slug)

        if type(saison) == Festival:
            liste_evenement = Evenement.objects.select_related().order_by('-haut_page').filter(fin__gt=datetime.datetime.now()).filter(publish=1).filter(cadre_evenement_id=saison.id)
            isfestival = "True"
        else:
            evenements = Evenement.objects.select_related(depth=1).filter(fin__gt=datetime.datetime.now()).filter(publish=1)
            festival = Festival.objects.select_related().filter(saison_culture_id=saison.id)
            
            filtre = Q(cadre_evenement_id=saison.id)
            for each in festival:
                filtre.add(Q(cadre_evenement_id=each.id), 'OR')
                
            liste_evenement = evenements.order_by('-haut_page').filter(filtre)
            isfestival = "False"
        
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/saison-details.html', {'liste_evenement': liste_evenement, 'saison': saison, 'isfestival': isfestival})

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

def EvenementDetailsHtml(request, slug, evenement_slug):
    try:
        saison = Saison.objects.get(slug=slug)
        evenement = Evenement.objects.select_related(depth=1).get(slug=evenement_slug)
        tarifs = Tarification.objects.filter(evenement_id=evenement.id)
        liste_lieux = evenement.lieu.select_related(depth=1).all()
        liste_equipements = Equipement.objects.select_related(depth=1).all()
        evenement_qr = GenerationQrCode(EvenementDetailsIcalendar(evenement))
        
        ListeLieux = list()
        
        for each in liste_lieux:
            correspondance = True
            for eachEquipement in liste_equipements:
                if eachEquipement.id == each.id:
                    ListeLieux.append(eachEquipement)
                    correspondance = False
            if correspondance:
                ListeLieux.append(each)

        localisation_qr = list()
        for each in liste_lieux:
            localisation_qr.append(GenerationQrCode("geo:"+str(each.latitude)+","+str(each.longitude)))

        #<trash>
        try:
            tarifs = tarifs[0]
        except:
            tarifs = None
        #</trash>  
    except SaisonCulturelle.DoesNotExist:
        raise Http404
    return render_to_response('evenements/evenement-details.html', {'evenement': evenement, 'saison': saison, 'tarifs': tarifs, 'evenement_qr': evenement_qr, 'localisation_qr': localisation_qr,'liste_lieux': ListeLieux })



def EvenementDetailsICS(request, slug, evenement_slug, festival_slug = None):
    try:
        evenement = Evenement.objects.select_related(depth=1).get(slug=evenement_slug)
        myText = EvenementDetailsIcalendar(evenement)
    except Evenement.DoesNotExist:
        raise Http404
    return HttpResponse(myText,content_type="text/calendar")
    #return render_to_response('evenements/evenement-details.ics.html', {'evenement': evenement})