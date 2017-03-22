# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^get-token.html$', views.mailJetGetToken, name="mailjet-get-token"),
    url(r'^mailjet-ajax.html$', views.mailJetAjax, name="mailjet-ajax"),
    url(r'^mailjet-post.html$', views.mailJetPost, name="mailjet-post"),
    url(r'^mailjet-reponse-(?P<reponse>[^\/]+).html$', views.mailJetReponse, name="mailjet-reponse"),
    url(r'^validation/(?P<hash>[^\/]+).html$', views.mailValidation, name="mail-validation"),
    url(r'^$', views.mailForm, name="mail-form"),
]