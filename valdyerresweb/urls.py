# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'essai.views.home', name='home'),
    # url(r'^essai/', include('essai.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^agenda/', include('evenements.urls')),
    url(r'^equipements/', include('equipements.urls')),
    url(r'^cinemas/', include('cinemas.urls')),
    url(r'^services/', include('services.urls')),
    url(r'^annoncesemploi/', include('annoncesemploi.urls')),
    url(r'^debug/', include('debug_toolbar.urls')),
    url(r'^mail/', include('lettreinformations.urls')),
    url(r'', include('editorial.urls')),
    url(r'^robots\.txt$', direct_to_template,{'template': 'robots.txt', 'mimetype': 'text/plain'}),
)
