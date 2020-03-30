"""Defines URL patterns for learning_logs."""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]
