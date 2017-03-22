from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^facilites/(?P<slug>[^\/]+).html$', views.FaciliteCarte, name="facilite-carte"),
    url(r'^facilites/$',views.FaciliteListe),
    
    url(r'^tarifs/(?P<equipement_fonction_slug>[^\/]+).html$', views.EquipementFonctionTarifs , name='equipement-fonction-tarifs'),
    url(r'^tarifs/$', views.EquipementTarifs , name='equipement-tarifs'),
    
    url(r'^horaires/(?P<equipement_slug>[^\/]+).html', views.EquipementHoraires, name="equipement-horaires"),
    url(r'^horaires/', views.HorairesTousEquipements, name="horaires-tous-equipements"),
    
    url(r'^alertes/alertes-ajax.html', views.AlertesAjax, name="alertes-ajax"),
    url(r'^alertes/get-token.html', views.AlertesGetToken, name="alertes-get-token"),
    url(r'^alertes/alertes-post-(?P<equipement_slug>[^\/]+).html', views.AlertesSansJs, name="alertes-sans-js"),
    url(r'^alertes/alertes-reponse-(?P<reponse>[0-9])-(?P<equipement>[^\/]+).html', views.AlertesReponse, name="alertes-reponse"),
    
    url(r'^$', views.EquipementsCarte),
    url(r'^(?P<fonction_slug>[^\/]+)/(?P<equipement_slug>[^\/]+).html$', views.EquipementsDetailsHtml, name="equipement-details"),
    url(r'^(?P<fonction_slug>[^\/]+)/$', views.FonctionDetailsHtml),
    url(r'^(?P<slug>[^\/]+).vcf$', views.EquipementVCF),
]