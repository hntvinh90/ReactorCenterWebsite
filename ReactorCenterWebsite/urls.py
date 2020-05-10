"""ReactorCenterWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HomePage.urls', 'homepage')),
    path('accounts/', include('Accounts.urls', 'accounts')),
    path('events/', include('Events.urls', 'events')),
    path('operation_timing/', include('OperationTiming.urls', 'operation_timing')),
    path('excess_reactivity/', include('ExcessReactivity.urls', 'excess_reactivity')),
    path('library/', include('Library.urls', 'library')),
]

# Add static url when DEBUG=False
if not settings.DEBUG:
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

# Add media url
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
