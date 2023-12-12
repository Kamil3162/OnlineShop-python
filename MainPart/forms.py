from django.contrib.auth.models import User, make_password
from django import forms
from .models import CustomUser


class LoginForm(forms.ModelForm):
    username = forms.EmailField(required=True)
    password = forms.CharField(max_length=60, required=True,  widget=forms.PasswordInput(attrs={'type': 'password'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegisterForm(forms.ModelForm):
    surname = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=40, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=60, required=True,
                               widget=forms.PasswordInput(attrs={'type': 'password'}
                                                          ))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'surname', 'password']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
