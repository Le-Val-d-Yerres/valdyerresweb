# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.AgendaGlobal, name='agenda-global'),
    url(r'^mois.ics$', views.AgendaNowICS),
    url(r'^organisateur/$', views.OrganisateurRedirect, name='organisateur_redirect'),
    url(r'^organisateur/(?P<organisateur_slug>[^\/]+).html$', views.OrganisateurDetailsHtml, name='organisateur_html'),
    url(r'^organisateur/(?P<organisateur_slug>[^\/]+).vcf$', views.OrganisateurVCF, name='organisateur_vcf'),
    # url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/$', 'AgendaMois', name="agenda-mois"),
    url(r'^(?P<annee>\d{4})/(?P<mois>\d{2})/mois.ics$', views.AgendaMoisICS),
    url(r'^type/(?P<type_slug>[^\/]+)/$', views.AgendaListTypePeriodOrga, name='agenda-type-period-orga'),
    url(r'^type/$', views.AgendaTypeRedirect, name='agenda-type-redirect'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/$', views.AgendaListTypePeriodOrga,
        name='agenda-type-period-orga'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/$', views.AgendaPeriodRedirect, name='agenda-period-redirect'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/orga/(?P<orga_slug>[^\/]+)/$',
        views.AgendaListTypePeriodOrga, name='agenda-type-period-orga'),
    url(r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/orga/$', views.AgendaOrgaRedirect,
        name='agenda-orga-redirect'),
    #   TODO : Le OR est a creuser pour un meilleur polymorphisme sur cette vue :
    #   url(r'^(type/(?P<type_slug>[^\/]+))|(periode/(?P<period>[^\/]+))|(orga/(?P<orga_slug>[^\/]+))/$','ListTypePeriodOrga',name='agenda-type-period-orga'),
    url(
        r'^type/(?P<type_slug>[^\/]+)/periode/(?P<period>[^\/]+)/orga/(?P<orga_slug>[^\/]+)/export.(?P<extension>[^\/]+)$',
        views.ExportAgendaListTypePeriodOrga, name='export-agenda-type-period-orga'),
    # url(r'^(?P<annee>\d{4})/$', 'AgendaAnnee', name='agenda-annee'),
    url(r'^(?P<annee>\d{4}).ics$', views.AgendaAnneeICS),
    url(r'^(?P<slug>[^\/]+)/$', views.SaisonDetailsHtml, name='saison-details'),
    url(r'^(?P<slug>[^\/]+)/export.(?P<extension>[^\/]+)$', views.SaisonDetailsHtmlExport, name='saison-details-export'),
    url(r'^(?P<slug>[^\/]+).ics$', views.SaisonDetailsICS),
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).html$', views.EvenementDetailsHtml, name="event-details"),
    url(r'^(?P<slug>[^\/]+)/(?P<evenement_slug>[^\/]+).ics$', views.EvenementDetailsICS, name="event-details-ics")
]
