"""Defines URL patterns for learning_logs."""
from django.urls import path

from . import views

app_name = 'operation_timing'

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.query, name='query'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete'),
]
