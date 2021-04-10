from django.urls import path

from .views import *
from .python_scripts.parse_coordinates import *

app_name = "world"

urlpatterns = [
    path('', MarkersMapView.as_view()),
    path('display_coordinates', display_coordinates),
    path('display_hypsometric', HypsometricMapView.as_view()),
    path('parse_coordinates', parse_coordinates),
]
