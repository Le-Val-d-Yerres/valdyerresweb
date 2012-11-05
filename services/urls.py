from django.conf.urls import patterns, include, url

urlpatterns = patterns('services.views',
    url(r'^$', 'ListeServices', name = "service-liste"),
    url(r'^(?P<service_slug>[^\/]+)/$', 'ServiceDetail', name = "service-detail"),
    url(r'^(?P<service_slug>[^\/]+)/(?P<page_slug>[^\/]+).html$', 'PageContenu', name="page-contenu"),  
)