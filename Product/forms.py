from .models import (ShipAddress,
                     Rate)
from django.forms import ModelForm

class ShipForm(ModelForm):
    class Meta:
        model = ShipAddress
        fields = '__all__'
        exclude = ('user', 'order')


class RateForm(ModelForm):
    class Meta:
        model = Rate
        exclude = ('product', 'user')
