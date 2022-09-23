from django.conf import settings
from django.db import models

from users.models import User

GENDER_CHOICE = (
    ("male", "Male"),
    ("female", "Female"),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        blank=True,
        null=True
    )
    gender = models.CharField(max_length=100, choices=GENDER_CHOICE, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True, default="")
    last_name = models.CharField(max_length=100, blank=True, null=True, default="")
    patronymic = models.CharField(max_length=100, blank=True, null=True, default="")
    phone_number = models.CharField(max_length=100, blank=True, null=True, default="")
    social_network_link = models.CharField(max_length=100, blank=True, null=True, default="")
    slug = models.SlugField(blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Profile for {self.user}"
