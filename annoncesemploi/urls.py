from django.conf.urls import patterns, include, url

urlpatterns = patterns('annoncesemploi.views',
    url(r'^$', 'AnnoncesList', name="annonces-list"),
    url(r'^(?P<service_slug>[^\/]+)/$', 'AnnoncesListService', name="annonces-list-service"),
    url(r'^annonce/(?P<annonce_slug>[^\/]+).html$', 'AnnonceDetail', name="annonce-detail"),
    
    
)