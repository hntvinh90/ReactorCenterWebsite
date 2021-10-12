"""Defines URL patterns for learning_logs."""
from django.urls import path

from . import views

app_name = 'operation_timing'

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.query, name='query'),
    path('get_files_and_folders', views.get_files_and_folders, name='get_files_and_folders'),
    path('append_data_from_file', views.append_data_from_file, name='append_data_from_file'),
]
