"""Custom storage backend for Supabase Storage."""

from django.conf import settings
from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from storage3 import create_client


class SupabaseStorage(Storage):
    """Django storage backend for Supabase Storage."""

    def __init__(self) -> None:
        """Initialize Supabase storage client."""
        self.supabase_url = getattr(settings, "SUPABASE_URL", "")
        self.supabase_key = getattr(settings, "SUPABASE_SERVICE_KEY", "")
        self.bucket_name = getattr(settings, "SUPABASE_STORAGE_BUCKET", "media")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")

        # storage3 expects the storage API URL and explicit auth headers,
        # rather than the project URL plus a key. Build them once.
        storage_url = f"{self.supabase_url}/storage/v1"
        headers = {
            "apiKey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
        }
        self.client = create_client(storage_url, headers, is_async=False)

    def _get_public_url(self, name: str) -> str:
        """Get public URL for a file."""
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"

    def _get_content_type(self, content: File) -> str:
        """Determine content type from file."""
        content_type = getattr(content, "content_type", "application/octet-stream")
        filename = getattr(content, "name", None)
        if filename:
            filename_lower = filename.lower()
            if filename_lower.endswith((".jpg", ".jpeg")):
                content_type = "image/jpeg"
            elif filename_lower.endswith(".png"):
                content_type = "image/png"
            elif filename_lower.endswith(".gif"):
                content_type = "image/gif"
            elif filename_lower.endswith(".webp"):
                content_type = "image/webp"
        return content_type

    def _save(self, name: str, content: File) -> str:
        """Save file to Supabase Storage."""
        file_content = content.read()
        content_type = self._get_content_type(content)
        self.client.from_(self.bucket_name).upload(
            path=name,
            file=file_content,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return name

    def _open(self, name: str, mode: str = "rb") -> ContentFile:
        """Open file from Supabase Storage."""
        response = self.client.from_(self.bucket_name).download(name)
        return ContentFile(response)

    def delete(self, name: str) -> None:
        """Delete file from Supabase Storage."""
        self.client.from_(self.bucket_name).remove([name])

    def exists(self, name: str) -> bool:
        """Check if file exists in Supabase Storage."""
        try:
            self.client.from_(self.bucket_name).download(name)
            return True
        except Exception:
            return False

    def url(self, name: str | None) -> str:
        """Get public URL for file."""
        if name is None:
            return ""
        return self._get_public_url(name)

    def size(self, name: str) -> int:
        """Get file size."""
        response = self.client.from_(self.bucket_name).download(name)
        return len(response)
