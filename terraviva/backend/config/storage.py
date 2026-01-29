"""Custom storage backend for Supabase Storage."""

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from supabase import create_client


class SupabaseStorage(Storage):
    """Django storage backend for Supabase Storage."""

    def __init__(self) -> None:
        """Initialize Supabase client."""
        self.supabase_url = getattr(settings, "SUPABASE_URL", "")
        self.supabase_key = getattr(settings, "SUPABASE_SERVICE_KEY", "")
        self.bucket_name = getattr(settings, "SUPABASE_STORAGE_BUCKET", "media")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

        self.client = create_client(self.supabase_url, self.supabase_key)

    def _get_public_url(self, name: str) -> str:
        """Get public URL for a file."""
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"

    def _save(self, name: str, content: File) -> str:
        """Save file to Supabase Storage."""
        file_content = content.read()

        # Determine content type
        content_type = getattr(content, "content_type", "application/octet-stream")
        if hasattr(content, "name"):
            if content.name.endswith(".jpg") or content.name.endswith(".jpeg"):
                content_type = "image/jpeg"
            elif content.name.endswith(".png"):
                content_type = "image/png"
            elif content.name.endswith(".gif"):
                content_type = "image/gif"
            elif content.name.endswith(".webp"):
                content_type = "image/webp"

        # Upload to Supabase
        self.client.storage.from_(self.bucket_name).upload(
            path=name,
            file=file_content,
            file_options={"content-type": content_type, "upsert": "true"},
        )

        return name

    def _open(self, name: str, mode: str = "rb") -> ContentFile:
        """Open file from Supabase Storage."""
        response = self.client.storage.from_(self.bucket_name).download(name)
        return ContentFile(response)

    def delete(self, name: str) -> None:
        """Delete file from Supabase Storage."""
        self.client.storage.from_(self.bucket_name).remove([name])

    def exists(self, name: str) -> bool:
        """Check if file exists in Supabase Storage."""
        try:
            self.client.storage.from_(self.bucket_name).download(name)
            return True
        except Exception:
            return False

    def url(self, name: str) -> str:
        """Get public URL for file."""
        return self._get_public_url(name)

    def size(self, name: str) -> int:
        """Get file size."""
        response = self.client.storage.from_(self.bucket_name).download(name)
        return len(response)
