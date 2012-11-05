# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('editorial.views',
    url(r'^$', 'Home', name="home"),
    url(r'^actualite/$', 'ActuLists', name="actu-liste"),
    url(r'^actualite/(?P<actualite_slug>[^\/]+).html$', 'ActuDetail', name="actu-detail"),
    url(r'^page/(?P<page_slug>[^\/]+).html$', 'PageDetail' , name="page-detail"),
   
    
)
    