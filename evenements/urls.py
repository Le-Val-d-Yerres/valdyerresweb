from django.conf.urls import patterns, include, url

urlpatterns = patterns('evenements.views',
    url(r'^$', 'Agenda'),
    url(r'^(?P<saison_slug>[^\/]+)/$', 'SaisonDetailsHtml'),
    url(r'^(?P<saison_slug>[^\/]+)/evenement/(?P<evenement_slug>[^\/]+).html$', 'SaisonEvenementDetailsHtml'),
    url(r'^(?P<saison_slug>[^\/]+)/(?P<festival_slug>[^\/]+)/(?P<evenement_slug>[^\/]+).html$', 'SaisonFestivalEvenementDetailsHtml'),
    url(r'^(?P<saison_slug>[^\/]+)/(?P<festival_slug>[^\/]+)/$', 'SaisonFestivalDetailsHtml'),
)