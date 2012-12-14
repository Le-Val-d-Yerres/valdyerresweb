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
    now = datetime.now(myTimezone)
    seances = Seance.objects.select_related().filter(date_debut__gt = now).order_by('film__titre','cinema__nom','date_debut')
    return render_to_response('cinemas/seances.html', {'seances' : seances})