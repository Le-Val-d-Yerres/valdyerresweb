from django.forms import ModelForm
from models import Stage,Disciplinestagecrd,Fichestagecrd

class FicheForm(ModelForm):
    class Meta:
        model = Fichestagecrd
        inlines = Stage()
