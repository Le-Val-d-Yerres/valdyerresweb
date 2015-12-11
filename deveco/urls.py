from django.conf.urls import patterns, include, url

urlpatterns = patterns('deveco.views',
                       url(r'^$', "home", name="home"),
                       url(r'^entreprise/(?P<slug>[^\/]+).html$', 'entreprise', name='entreprise'),
                       url(r'^entreprisevcard/(?P<slug>[^\/]+).vcf', 'entreprisevcard', name='entreprisevcard')

                       )
