"""Defines URL patterns for learning_logs."""
from django.urls import path

from . import views

# If namespace is available in global urls
app_name = 'excess_reactivity'

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.index, name='query'),
    path('get_files_and_folders', views.get_files_and_folders, name='get_files_and_folders'),
    path('append_data_from_file', views.append_data_from_file, name='append_data_from_file'),
]
