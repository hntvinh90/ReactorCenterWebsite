"""Defines URL patterns for learning_logs."""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

# If namespace is available in global urls
app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('query/', views.query, name='query'),
    path('append_data_from_file', views.append_data_from_file, name='append_data_from_file'),
] + static('/query/', document_root=settings.EVENTS_ROOT)
