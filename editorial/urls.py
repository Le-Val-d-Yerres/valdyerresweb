# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from .import views

urlpatterns = [
    url(r'^$', views.Home, name="home"),
    url(r'^actualite/$', views.ActuList, name="actulist"),
    url(r'^actualite/(?P<actualite_slug>[^\/]+).html$', views.ActuDetail, name="actudetail"),
    url(r'^page/(?P<page_slug>[^\/]+).html$', views.PageDetail , name="page-detail"),
    url(r'^magazines/$', views.Magazines , name="magazines"),
    url(r'^magazines/(?P<page>[^\/]+)$', views.Magazines , name="magazines"),
    url(r'^rapports/$', views.Rapports , name="rapports"),
    url(r'^rapports/(?P<page>[^\/]+)$', views.Rapports, name="rapports"),
    url(r'^ephemeride/(?P<jour>[^\/]+).html$', views.Ephemeride, name="ephemeride"),
    url(r'^ephemeride/$', views.Ephemeride, name="ephemeride"),
    url(r'^newsletters/(?P<equipement_slug>[^\/]+).html$', views.newsletterbibhtml, name='newsletterbibhtml'),
    url(r'^newsletters/', views.newsletterbiblist, name="newsletterbiblist"),
    url(r'^elus/', views.elus, name='elus'),
    url(r'^comptes-rendus/',views.comptesrendus, name='compterendus' )

]