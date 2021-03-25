from django.shortcuts import render
from django.views.generic.base import TemplateView

from .forms import *

# Create your views here.


class MarkersMapView(TemplateView):
    """Markers map view."""
    template_name = "map.html"