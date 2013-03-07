from django.conf.urls import patterns, include, url

urlpatterns = patterns('equipements.views',
    url(r'^facilites/((?P<slug>[^\/]+).html)$','CarteFacilite'),
    url(r'^tarifs/(?P<equipement_fonction_slug>[^\/]+).html$', 'EquipementFonctionTarifs' , name='equipement-fonction-tarifs'),
    url(r'^horaires/(?P<equipement_slug>[^\/]+).html', 'EquipementHoraires', name="equipement-horaires"),
    url(r'^$', 'CarteEquipements'),
    url(r'^(?P<fonction_slug>[^\/]+)/(?P<equipement_slug>[^\/]+).html$', 'EquipementsDetailsHtml', name="equipement-details"),
    url(r'^(?P<fonction_slug>[^\/]+)/$', 'FonctionDetailsHtml'),
    url(r'^(?P<slug>[^\/]+).vcf$', 'EquipementVCF'),
   
    
)
    