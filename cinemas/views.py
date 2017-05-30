# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse ,HttpResponseGone
from django.shortcuts import render_to_response , redirect , get_object_or_404
from cinemas.models import Cinema,Film,Seance
from cinemas.lib import eventAddlink
from django.template import Context, loader
from pytz import timezone
from datetime import datetime
from valdyerresweb import settings
from valdyerresweb.utils.functions import GenerationQrCode


utcTZ = timezone("UTC")
myTimezone = timezone(settings.TIME_ZONE)


def Seances(request):
    now = datetime.now(myTimezone)
    seances = Seance.objects.select_related().filter(date_debut__gt = now).order_by('film__id','cinema__nom','date_debut')
    return render_to_response('cinemas/seances.html', {'seances' : seances})

def CinemaLieu(request,cinema_slug):
    now = datetime.now(myTimezone)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    seances = Seance.objects.select_related().filter(cinema__slug = cinema_slug ,date_debut__gt = now).order_by('film__id','cinema__nom','date_debut')
    qr_code_vcard = GenerationQrCode(CinemaVcard(cinema))
    qr_code_geo = GenerationQrCode("geo:" + str(cinema.latitude) + "," + str(cinema.longitude))
    return render_to_response('cinemas/cinema-details.html', {'cinema':cinema ,'seances' : seances, 'qr_code_vcard': qr_code_vcard, 'qr_code_geo':qr_code_geo})

def CinemaVcard(cinema):
    myTemplate = loader.get_template('cinemas/cinema.vcf.html')
    myContext = {"cinema": cinema, "settings": settings}
    return myTemplate.render(myContext)

def CinemaVCF(request,cinema_slug):
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    myVcard = CinemaVcard(cinema)
    return HttpResponse(myVcard, content_type="text/vcard")

def SeanceIcalendar(seance):
    myTemplate = loader.get_template('cinemas/seance.ics.html')
    myContext = {"seance": seance, "settings": settings}
    return myTemplate.render(myContext)

def SeanceICS(request,seance_id):
    seance = get_object_or_404(Seance, id = seance_id)
    myICS = SeanceIcalendar(seance)
    return HttpResponse(myICS, content_type="text/calendar")

def SeanceAddAgenda(request,seance_id):
    try:
        seance = Seance.objects.get(id=seance_id)
    except Seance.DoesNotExist:
        myTemplate = loader.get_template("410.html")
        message = "Cette séance de cinéma n'est plus disponible "
        myContext = {"message":message}
        return HttpResponse(myTemplate.render(myContext),status=410)
    qr_code_geo = GenerationQrCode("geo:" + str(seance.cinema.latitude) + "," + str(seance.cinema.longitude))
    qr_code_calendar = GenerationQrCode(SeanceIcalendar(seance))
    return render_to_response('cinemas/seance-add-calendar.html', {'seance' : seance, 'qr_code_calendar': qr_code_calendar, 'qr_code_geo':qr_code_geo})
    
    
    
    
    