# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('cinemas.views',
    url(r'^$', 'Seances', name="seances"),
    url(r'^(?P<cinema_slug>[^\/]+).html$', 'CinemaLieu', name="cinema"),
    url(r'^(?P<cinema_slug>[^\/]+).vcf$', 'CinemaVCF', name="cinemavcf"),
    url(r'^(?P<seance_id>[^\/]+).ics$', 'SeanceICS', name="seanceics"),
    url(r'^add/(?P<seance_id>[^\/]+).html$', 'SeanceAddAgenda', name="seanceaddagenda"),
    
)
    