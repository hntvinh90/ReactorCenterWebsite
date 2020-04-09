"""Defines URL patterns for learning_logs."""
from django.urls import path

from . import views

# If namespace is available in global urls
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_files_and_folders', views.get_files_and_folders, name='get_files_and_folders'),
    path('search', views.search, name='search'),
]
