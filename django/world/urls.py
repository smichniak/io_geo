from django.urls import path

from .views import *

app_name = "world"

urlpatterns = [
    path('', MarkersMapView.as_view()),
    path('draw_data', draw_data),
]
