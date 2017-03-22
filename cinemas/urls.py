# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.Seances, name="seances"),
    url(r'^(?P<cinema_slug>[^\/]+).html$', views.CinemaLieu, name="cinema"),
    url(r'^(?P<cinema_slug>[^\/]+).vcf$', views.CinemaVCF, name="cinemavcf"),
    url(r'^(?P<seance_id>[^\/]+).ics$', views.SeanceICS, name="seanceics"),
    url(r'^add/(?P<seance_id>[^\/]+).html$', views.SeanceAddAgenda, name="seanceaddagenda"),
    ]
