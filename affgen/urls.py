from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from .import views

urlpatterns = [
    url(r'^$',views.homeaffgen, name='homeaffgen'),
    url(r'^elus/', views.elus, name='elus'),
    url(r'^comptes-rendus/$', views.comptesrendus, name='comptesrendus'),
    url(r'^comptes-rendus/(?P<idcpt>[^\/]+).html$', views.compterendu, name='compterendu')
]

