from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile/", default="profile/default.jpg", blank=True
    )
    phone_number = models.CharField(max_length=11, blank=True)

    def __str__(self):
        return self.username
