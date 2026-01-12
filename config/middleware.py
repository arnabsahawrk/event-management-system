from whitenoise.middleware import WhiteNoiseMiddleware as BaseWhiteNoiseMiddleware
from django.conf import settings


class WhiteNoiseMediaMiddleware(BaseWhiteNoiseMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(settings, "MEDIA_ROOT") and hasattr(settings, "MEDIA_URL"):
            media_root = str(settings.MEDIA_ROOT)
            media_url = settings.MEDIA_URL
            if media_url.startswith("/"):
                media_url = media_url[1:]
            self.add_files(media_root, prefix=media_url)
