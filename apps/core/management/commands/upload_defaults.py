from django.core.management.base import BaseCommand
from django.conf import settings
import cloudinary.uploader


class Command(BaseCommand):
    help = "Upload default placeholder images to Cloudinary"

    def handle(self, *args, **options):
        defaults = [
            (settings.MEDIA_ROOT / "events" / "default.jpg", "events/default"),
            (settings.MEDIA_ROOT / "profile" / "default.jpg", "profile/default"),
        ]

        for local_path, public_id in defaults:
            self.stdout.write(f"\nLooking for: {local_path}")

            if local_path.exists():
                self.stdout.write("  Found!")
                try:
                    result = cloudinary.uploader.upload(
                        str(local_path),
                        public_id=public_id,
                        overwrite=True,
                        resource_type="image",
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"  OK: {result['secure_url']}")
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  FAILED: {e}"))
            else:
                self.stdout.write(self.style.ERROR("  NOT FOUND."))

        self.stdout.write(self.style.SUCCESS("\nDone!"))
