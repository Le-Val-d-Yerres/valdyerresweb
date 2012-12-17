# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response , redirect , get_object_or_404
from cinemas.models import Cinema,Film,Seance
from django.template import Context, loader
from pytz import timezone
from datetime import datetime
from valdyerresweb import settings
from valdyerresweb.utils.functions import GenerationQrCode


utcTZ = timezone("UTC")
myTimezone = timezone(settings.TIME_ZONE)


def Seances(request):
    now = datetime.now(myTimezone)
    seances = Seance.objects.select_related().filter(date_debut__gt = now).order_by('film__titre','cinema__nom','date_debut')
    return render_to_response('cinemas/seances.html', {'seances' : seances})



def CinemaLieu(request,cinema_slug):
    now = datetime.now(myTimezone)
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    seances = Seance.objects.select_related().filter(cinema__slug = cinema_slug ,date_debut__gt = now).order_by('film__titre','cinema__nom','date_debut')
    qr_code_vcard = GenerationQrCode(CinemaVcard(cinema))
    qr_code_geo = GenerationQrCode("geo:" + str(cinema.latitude) + "," + str(cinema.longitude))
    return render_to_response('cinemas/cinema-details.html', {'cinema':cinema ,'seances' : seances, 'qr_code_vcard': qr_code_vcard, 'qr_code_geo':qr_code_geo})

def CinemaVCF(request,cinema_slug):
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    myVcard = CinemaVcard(cinema)
    return HttpResponse(myVcard, content_type="text/vcard")


def CinemaVcard(cinema):
    myTemplate = loader.get_template('cinemas/cinema.vcf.html')
    myContext = Context({"cinema": cinema, "settings": settings})
    return myTemplate.render(myContext)