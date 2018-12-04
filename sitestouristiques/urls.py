from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^site/(?P<equipement_slug>[^\/]+).html', views.site, name="site"),
    url(r'^$', views.list, name="list"),
]