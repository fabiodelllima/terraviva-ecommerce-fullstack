"""
Product services - Business logic layer.

This module contains business logic for product-related operations,
following Single Responsibility Principle.
"""

import os
from io import BytesIO
from typing import Any

from django.core.files import File
from PIL import Image


class ImageService:
    """
    Service for image processing operations.

    Extracts image manipulation logic from models,
    following Single Responsibility Principle.
    """

    DEFAULT_THUMBNAIL_SIZE: tuple[int, int] = (300, 200)
    DEFAULT_QUALITY: int = 85
    DEFAULT_FORMAT: str = "JPEG"

    @classmethod
    def make_thumbnail(
        cls,
        image: Any,
        size: tuple[int, int] | None = None,
        quality: int | None = None,
    ) -> File:
        """
        Create a thumbnail from an image.

        Args:
            image: Source image (ImageFieldFile or file-like object)
            size: Thumbnail dimensions (width, height)
            quality: JPEG quality (1-100)

        Returns:
            Django File object containing the thumbnail
        """
        size = size or cls.DEFAULT_THUMBNAIL_SIZE
        quality = quality or cls.DEFAULT_QUALITY

        img = Image.open(image)
        img = img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, cls.DEFAULT_FORMAT, quality=quality)
        thumb_io.seek(0)

        filename = os.path.basename(image.name)
        return File(thumb_io, name=filename)

    @staticmethod
    def get_safe_url(field: Any) -> str:
        """
        Safely extract URL from ImageFieldFile.

        Args:
            field: Django ImageField or similar

        Returns:
            URL string or empty string if not available
        """
        if not field:
            return ""
        try:
            url = getattr(field, "url", None)
            return str(url) if url else ""
        except Exception:
            return ""
