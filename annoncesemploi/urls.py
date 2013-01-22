from django.conf.urls import patterns, include, url

urlpatterns = patterns('annoncesemploi.views',
    url(r'^$', 'AnnoncesList', name="annonces-list"),
    url(r'^annonce/(?P<annonce_slug>[^\/]+).html$', 'AnnonceDetail', name="annonce-detail"),
    
    
)