# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from .import views

urlpatterns = [
    url(r'^$', 'Home', name="home"),
    url(r'^actualite/$', 'ActuList', name="actu-list"),
    url(r'^actualite/(?P<actualite_slug>[^\/]+).html$', 'ActuDetail', name="actu-detail"),
    url(r'^page/(?P<page_slug>[^\/]+).html$', 'PageDetail' , name="page-detail"),
    url(r'^magazines/$', 'Magazines' , name="magazines"),
    url(r'^magazines/(?P<page>[^\/]+)$', 'Magazines' , name="magazines"),
    url(r'^rapports/$', 'Rapports' , name="rapports"),
    url(r'^rapports/(?P<page>[^\/]+)$', 'Rapports' , name="rapports"),
    url(r'^ephemeride/(?P<jour>[^\/]+).html$', 'Ephemeride', name="ephemeride"),
    url(r'^ephemeride/$', 'Ephemeride', name="ephemeride"),
    url(r'^newsletters/(?P<equipement_slug>[^\/]+).html$','newsletterbibhtml', name='newsletterbibhtml'),
    url(r'^newsletters/', 'newsletterbiblist', name="newsletterbiblist"),
    url(r'^elus/', 'elus', name='elus')
]