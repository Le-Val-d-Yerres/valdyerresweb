from django.conf.urls import patterns, include, url

urlpatterns = patterns('editorial.views',
    url(r'^horaires/(?P<equipement_slug>[^\/]+).html', 'EquipementHoraires', name="equipement-horaires"),
    url(r'^$', 'home'),
    url(r'^(?P<fonction_slug>[^\/]+)/(?P<equipement_slug>[^\/]+).html$', 'EquipementsDetailsHtml', name="equipement-details"),
    url(r'^(?P<fonction_slug>[^\/]+)/$', 'FonctionDetailsHtml'),
    url(r'^(?P<slug>[^\/]+).vcf$', 'EquipementVCF'),
    
)
    