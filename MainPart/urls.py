from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('logo/',views.log_out, name="log_out"),
    path('indexpage/', views.indexpage, name='mainpage'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='registration')
    # path('bucket/', views.BucketView.as_view(), name='bucket')
]