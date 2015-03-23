from django.conf.urls import patterns, include, url

urlpatterns = patterns('equipements.views',
    url(r'^facilites/(?P<slug>[^\/]+).html$','FaciliteCarte', name="facilite-carte"),
    url(r'^facilites/$','FaciliteListe'),
    
    url(r'^tarifs/(?P<equipement_fonction_slug>[^\/]+).html$', 'EquipementFonctionTarifs' , name='equipement-fonction-tarifs'),
    url(r'^tarifs/$', 'EquipementTarifs' , name='equipement-tarifs'),
    
    url(r'^horaires/(?P<equipement_slug>[^\/]+).html', 'EquipementHoraires', name="equipement-horaires"),
    url(r'^horaires/', 'HorairesTousEquipements', name="horaires-tous-equipements"),
    
    url(r'^alertes/alertes-ajax.html', 'AlertesAjax', name="alertes-ajax"),
    url(r'^alertes/get-token.html', 'AlertesGetToken', name="alertes-get-token"),
    url(r'^alertes/alertes-post-(?P<equipement_slug>[^\/]+).html', 'AlertesSansJs', name="alertes-sans-js"),
    url(r'^alertes/alertes-reponse-(?P<reponse>[0-9])-(?P<equipement>[^\/]+).html', 'AlertesReponse', name="alertes-reponse"),
    
    url(r'^$', 'EquipementsCarte'),
    url(r'^(?P<fonction_slug>[^\/]+)/(?P<equipement_slug>[^\/]+).html$', 'EquipementsDetailsHtml', name="equipement-details"),
    url(r'^(?P<fonction_slug>[^\/]+)/$', 'FonctionDetailsHtml'),
    url(r'^(?P<slug>[^\/]+).vcf$', 'EquipementVCF'),
)