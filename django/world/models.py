from django.db import models
from django.contrib.gis.db.models import PointField


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = PointField()


class HypsometricImages(models.Model):
    image = models.ImageField(upload_to='uploaded_images')
