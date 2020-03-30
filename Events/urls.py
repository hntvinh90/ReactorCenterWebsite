"""Defines URL patterns for learning_logs."""
from django.urls import path

from . import views

# If namespace is available in global urls
app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('query_event/', views.query_event, name='query_event'),
    path('add_event/', views.add_event, name='add_event'),
    path('del_event/', views.del_event, name='del_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
]
