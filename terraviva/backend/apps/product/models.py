"""
Product models - Entity layer.

Models are kept thin, delegating business logic to services.
"""

from django.db import models

from .services import ImageService


class Category(models.Model):
    """Product category for organizing products."""

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
    """Product entity with category relationship."""

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

    def get_image(self) -> str:
        """Get product image URL."""
        return ImageService.get_safe_url(self.image)

    def get_thumbnail(self) -> str:
        """Get thumbnail URL, generating if needed."""
        thumb_url = ImageService.get_safe_url(self.thumbnail)
        if thumb_url:
            return thumb_url

        if self.image:
            try:
                self.thumbnail = ImageService.make_thumbnail(self.image)
                self.save()
                return ImageService.get_safe_url(self.thumbnail)
            except Exception:
                return ImageService.get_safe_url(self.image)
        return ""
