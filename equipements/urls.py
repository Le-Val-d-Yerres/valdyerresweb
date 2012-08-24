from django.conf.urls import patterns, include, url

urlpatterns = patterns('equipements.views',
    url(r'^$', 'CarteEquipements'),
    url(r'^(?P<fonction_slug>[^\/]+)/(?P<equipement_slug>[^\/]+).html$', 'EquipementsDetailsHtml'),
    url(r'^(?P<fonction_slug>[^\/]+)/$', 'FonctionDetailsHtml'),
)
    