# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('evenements.views',
    url(r'^$', 'AgendaGlobal', name='agenda-global'),
    url(r'^mois.ics$', 'AgendaNowICS'),
    
    url(r'^organisateur/(?P<organisateur_slug>[^\/]+).html$', 'OrganisateurDetailsHtml', name='organisateur_html'),
    url(r'^organisateur/(?P<organisateur_slug>[^\/]+).vcf$','OrganisateurVCF',  name='organisateur_vcf'),
    
    url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/$', 'AgendaMois', name="agenda-mois"),
    url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/mois.ics$', 'AgendaMoisICS'),
    
    url(r'^type/(?P<type_slug>[^\/]+)/$','ListTypePeriodOrga',name='agenda-type-period-orga'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/$','ListTypePeriodOrga',name='agenda-type-period-orga'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/orga/(?P<orga_slug>[^\/]+)/$','ListTypePeriodOrga',name='agenda-type-period-orga'),
 #   TODO : Le OR est a creuser pour un meilleur polymorphisme sur cette vue :
 #   url(r'^(type/(?P<type_slug>[^\/]+))|(periode/(?P<period>[^\/]+))|(orga/(?P<orga_slug>[^\/]+))/$','ListTypePeriodOrga',name='agenda-type-period-orga'),


    
    url(r'^(?P<annee>\d{4})/$', 'AgendaAnnee', name='agenda-annee'),
    url(r'^(?P<annee>\d{4}).ics$', 'AgendaAnneeICS'),
    
    url(r'^(?P<slug>[^\/]+)/$', 'SaisonDetailsHtml'),
    url(r'^(?P<slug>[^\/]+).ics$', 'SaisonDetailsICS'),
    
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).html$', 'EvenementDetailsHtml', name="event-details"),
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).ics$', 'EvenementDetailsICS', name ="event-details-ics"),
)