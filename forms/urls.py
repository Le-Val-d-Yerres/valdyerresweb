from django.conf.urls import patterns, include, url

urlpatterns = patterns('forms.views',

                       url(r'^form-crd.html$', 'formfichestage', name="formfichestage"),
                       url(r'^merci.html$', 'merci', name="merci"),
                       )
