from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^site/(?P<equipement_slug>[^\/]+).html', views.EquipementHoraires, name="equipement-horaires"),
    url(r'^$', views.EquipementsCarte, name="equipements-carte"),
]