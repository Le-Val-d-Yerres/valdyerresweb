import datetime
from haystack import indexes

from .models import Actualite

class ActualiteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titre = indexes.CharField(model_attr='titre')
    contenu = indexes.CharField(model_attr='contenu')
    date_publication = indexes.DateField(model_attr='date_publication')

    def get_model(self):
        return Actualite

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(publie=True)
