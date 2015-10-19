from django.conf.urls import patterns, include, url

urlpatterns = patterns('deveco.views',
    url(r'^$', 'Home', name="home"),
)
