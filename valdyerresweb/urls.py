# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from filebrowser.sites import site

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
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
    url(r'^mail/', include('lettreinformations.urls')),
    url(r'', include('editorial.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )