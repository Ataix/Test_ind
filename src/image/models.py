import os

from django.db import models
from django.urls import reverse


class ImageModel(models.Model):
    initial_image = models.ImageField(upload_to='images')
    result_json = models.JSONField(blank=True, null=True)
    result_image = models.ImageField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return str(os.path.split(self.initial_image.path)[-1])

    def get_absolute_url(self):
        return reverse("images:imageset_detail_url", kwargs={"pk": self.pk})
