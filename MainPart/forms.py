from django.contrib.auth.models import User
from django import forms
from .models import CustomUser


class LoginForm(forms.ModelForm):
    username = forms.EmailField(required=True)
    password = forms.CharField(max_length=60, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):
    surname = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=60, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'surname', 'password']




