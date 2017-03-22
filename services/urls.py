# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.Services, name = "services"),
    url(r'^(?P<service_slug>[^\/]+)/$', views.ServiceDetail, name = "service-detail"),
    url(r'^(?P<service_slug>[^\/]+)/(?P<page_slug>[^\/]+).html$', views.PageContenu, name="page-contenu"),
]