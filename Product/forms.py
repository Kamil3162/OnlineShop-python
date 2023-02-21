from .models import (ShipAddress,
                     Rate,
                     CardPayment)
from django import forms


class ShipForm(forms.ModelForm):
    class Meta:
        model = ShipAddress
        fields = '__all__'
        exclude = ('user', 'order')


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        exclude = ('product', 'user')


class ComplainForm(forms.Form):
    complait = 'Complain'
    product_return = 'Return'
    ship_problem = 'Ship'
    manufacturing_defect = 'Defect'

    topics = (
        (complait, 'Reklamacja'),
        (product_return, 'Zwrot - 14 dni'),
        (ship_problem, 'Gdzie moja paczka?'),
        (manufacturing_defect, 'Wada fabryczna')
    )

    user = forms.CharField(max_length=30, required=True)
    product = forms.CharField(max_length=60, required=True)
    order = forms.IntegerField(required=True)
    subject = forms.CharField(max_length=20, required=True,
                              widget=forms.Select(choices=topics))
    description = forms.CharField(max_length=200, widget=forms.Textarea)


