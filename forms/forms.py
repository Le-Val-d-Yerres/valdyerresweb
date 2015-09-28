from django.forms import ModelForm
from forms.models import Stage,Disciplinestagecrd,Fichestagecrd

class FicheForm(ModelForm):
    class Meta:
        model = Fichestagecrd
