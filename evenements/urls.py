# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('evenements.views',
    url(r'^$', 'AgendaGlobal'),
    url(r'^mois.ics$', 'AgendaNowICS'),
    
    url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/$', 'AgendaMois', name="agenda-mois"),
    url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/mois.ics$', 'AgendaMoisICS'),
    
    url(r'^type/(?P<type_slug>[^\/]+)/$','ListType',name='list-type'),
    url(r'^type/(?P<type_slug>[^\/]+)/cette-semaine/$','ListTypeWeek',name='list-type'),
    url(r'^type/(?P<type_slug>[^\/]+)/ce-week-end/$','ListTypeWeekEnd',name='list-type'),
    url(r'^type/(?P<type_slug>[^\/]+)/ce-mois/$','ListTypeMonth',name='list-type'),

    url(r'^type/$','ListAllType',name='list-all-type'),
    
    url(r'^(?P<annee>\d{4})/$', 'AgendaAnnee', name='agenda-annee'),
    url(r'^(?P<annee>\d{4}).ics$', 'AgendaAnneeICS'),
    
    url(r'^(?P<slug>[^\/]+)/$', 'SaisonDetailsHtml'),
    url(r'^(?P<slug>[^\/]+).ics$', 'SaisonDetailsICS'),
    
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).html$', 'EvenementDetailsHtml', name="event-details"),
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).ics$', 'EvenementDetailsICS', name ="event-details-ics"),
)