import os
from io import BytesIO
from typing import Any

from django.core.files import File
from django.db import models
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/{self.slug}/"


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return f"/{self.category.slug}/{self.slug}/"

    def _get_field_url(self, field: Any) -> str:
        """Safely extract URL from ImageFieldFile."""
        if field:
            try:
                url = getattr(field, "url", None)
                if url:
                    return str(url)
            except Exception:
                return ""
        return ""

    def get_image(self) -> str:
        return self._get_field_url(self.image)

    def get_thumbnail(self) -> str:
        thumb_url = self._get_field_url(self.thumbnail)
        if thumb_url:
            return thumb_url

        if self.image:
            try:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self._get_field_url(self.thumbnail)
            except Exception:
                # Image not accessible in storage, return main image URL
                return self._get_field_url(self.image)
        return ""

    def make_thumbnail(self, image: Any, size: tuple[int, int] = (300, 200)) -> File:
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        # Use only the filename, not the full path (upload_to handles the path)
        filename = os.path.basename(image.name)
        thumbnail = File(thumb_io, name=filename)

        return thumbnail
