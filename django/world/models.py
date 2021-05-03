from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from django.db import models
from django.contrib.gis.db.models import PointField


class Marker(models.Model):
    """A marker with name and location."""

    name = models.CharField(max_length=255)
    location = PointField()


class MapDetailsImages(models.Model):
    image_file = models.ImageField(null=True, upload_to='uploaded_images')
    image_url = models.URLField()

    class Meta:
        verbose_name_plural = "SurfaceDetailsImages"

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image_file.save(f"details_{self.pk}.jpeg", File(img_temp))
        self.save()


class HypsometricImages(models.Model):
    image = models.ImageField(blank=False, null=False, upload_to='uploaded_images')
    details_map = models.ForeignKey(MapDetailsImages, null=True, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "HypsometricImages"


class SurfaceImages(models.Model):
    image = models.ImageField(blank=False, null=False, upload_to='uploaded_images')

    class Meta:
        verbose_name_plural = "SurfaceImages"

