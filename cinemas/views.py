# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response , redirect , get_object_or_404
from cinemas.models import Cinema,Film,Seance
from pytz import timezone
from datetime import datetime
from valdyerresweb import settings

utcTZ = timezone("UTC")
myTimezone = timezone(settings.TIME_ZONE)


def Seances(request):
    now = datetime.now(utcTZ)
    seances = Seance.objects.select_related().filter(date_debut__gt = now)
    seances.order_by('date_debut')
    return render_to_response('cinemas/seances.html', {'seances' : seances})