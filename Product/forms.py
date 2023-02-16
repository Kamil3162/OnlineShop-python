from .models import ShipAddress
from django.forms import ModelForm

class ShipForm(ModelForm):
    class Meta:
        model = ShipAddress
        fields = '__all__'
        exclude = ('user', 'order')