from django.urls import path

from .views import MarkersMapView

app_name = "world"

urlpatterns = [
    path('', MarkersMapView.as_view()),
]
