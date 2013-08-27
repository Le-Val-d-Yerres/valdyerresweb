# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('lettreinformations.views',
    url(r'^get-token.html$', 'mailJetGetToken', name="mailjet-get-token"),               
    url(r'^mailjet-ajax.html$', 'mailJetAjax', name="mailjet-ajax"),
    url(r'^mailjet-post.html$', 'mailJetPost', name="mailjet-post"),
    url(r'^mailjet-reponse-(?P<reponse>[^\/]+).html$', 'mailJetReponse', name="mailjet-reponse"),
    url(r'^validation/(?P<hash>[^\/]+).html$', 'mailValidation', name="mail-validation"),
    url(r'^$', 'mailForm', name="mail-form"),
)