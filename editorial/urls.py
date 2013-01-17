# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('editorial.views',
    url(r'^$', 'Home', name="home"),
    url(r'^actualite/$', 'ActuList', name="actu-list"),
    url(r'^actualite/(?P<actualite_slug>[^\/]+).html$', 'ActuDetail', name="actu-detail"),
    url(r'^page/(?P<page_slug>[^\/]+).html$', 'PageDetail' , name="page-detail"),
    url(r'^magazines/$', 'Magazines' , name="magazines"),
    url(r'^magazines/(?P<page>[^\/]+)$', 'Magazines' , name="magazines"),
    url(r'^rapports/$', 'Rapports' , name="rapports"),
    url(r'^rapports/(?P<page>[^\/]+)$', 'Rapports' , name="rapports"),
    url(r'^ephemeride/(?P<jour>[^\/]+).html$', 'Ephemeride' , name="ephemeride"),
    
)