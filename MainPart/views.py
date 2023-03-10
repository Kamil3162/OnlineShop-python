from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import View
from MainPart import forms
from .models import CustomUser
from Product.models import (Category,
                            Producer)
# Create your views here.


def first_information(request):
    return render(request, "Base.html")

def access_categories(request):
    category = Category.objects.all()
    producents = Producer.objects.all()
    context = {
        'categories': category,
        'producents': producents
    }
    return context


def indexpage(request):
    return render(request, "Navbar.html")


def create_user(request):
    if request.method == "POST":
        print("register")
    register_form = forms.RegisterForm()
    return render(request, 'Register.html', {'register':register_form})

def login_auth(request):
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form)
            login_user = login_form.cleaned_data['login']
            password = login_form.cleaned_data['password']
            return redirect('information')
    login_form = forms.LoginForm()
    return render(request, 'Login.html', {'form': login_form})


class LoginView(View):
    template_name = "Login.html"
    form = forms.LoginForm

    def loginchecker(self, login_f: str) -> bool:
        user = CustomUser.objects.get(login=login_f)

        print("obj exist")
        if user:
            return True
        return False

    def get(self, request):
        print("this is get rqeuest")
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        if request.method == "POST":
            print("this is login profile")
            form = forms.LoginForm(request.POST)
            print(form.errors)
            print(form.fields)
            print(form.cleaned_data['password'])
            print(request.POST)
            if form.is_valid():
                login_1 = form.cleaned_data['username']
                password = form.cleaned_data['password']
                print(login_1, password)
                try:
                    user_auth = authenticate(request, username=login_1, password=password)
                    login(request, user_auth)
                    request.session['username'] = login_1
                    request.session['count_prod'] = 0
                    request.session['status'] = True
                    request.session.set_expiry(None)
                    print("data exists")
                    return redirect("information")
                except Exception:
                    print("No data")
        else:
            return redirect('login')
        return render(request, self.template_name, {'form':form})


class RegisterView(View):
    template_name = "Register.html"
    form = forms.RegisterForm

    """def duplicated_data(self, login_user: str, mail: str) -> bool:
        users_log = CustomUser.objects.all().get(login=login_user)
        user_adr = CustomUser.objects.acccll().get(email=mail)
        if users_log or user_adr:
            return True
        elif user_adr and users_log:
            return True
        return False
    """
    def get(self, request):
        form = self.form
        return render(request, self.template_name, {'register':form})

    def post(self, request):
        if request.method == "POST":
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                print("its goood")
                mail = form.cleaned_data['email']
                form.save()
                #except Exception:
                    #print("maybe user exist or you have another problem")
        return redirect("information")

    def data_validator(self, username):
        user = CustomUser.objects.get(email=username)
        print(user)
        if user:
            return False
        return True


def log_out(request):
    request.session.flush()
    logout(request)
    return redirect("information")