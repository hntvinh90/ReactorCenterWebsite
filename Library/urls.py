"""Defines URL patterns for learning_logs."""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

# If namespace is available in global urls
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_material', views.get_material, name='get_material'),
]
