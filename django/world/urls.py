from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .python_scripts.parse_coordinates_hypsometric import *

app_name = "world"

urlpatterns = [
                  path('', MarkersMapView.as_view()),
                  path('display_coordinates', display_coordinates),
                  path('display_hypsometric/<int:pk>/', HypsometricMapView.as_view()),
                  path('parse_coordinates_hypsometric', parse_coordinates_hypsometric),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
