from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.AnnoncesList, name="annonces-list"),
    url(r'^(?P<service_slug>[^\/]+)/$', views.AnnoncesListService, name="annonces-list-service"),
    url(r'^(?P<service_slug>[^\/]+)/(?P<annonce_slug>[^\/]+).html$', views.AnnonceDetail, name="annonce-detail"),
]