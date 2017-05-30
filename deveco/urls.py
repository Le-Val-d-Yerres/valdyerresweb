# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="homedeveco"),
    url(r'^entreprise/(?P<slug>[^\/]+).html$', views.entreprise, name='entreprise'),
    url(r'^entreprisevcard/(?P<slug>[^\/]+).vcf', views.entreprisevcard, name='entreprisevcard')
]
