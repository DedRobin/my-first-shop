from django.db import models

from users.models import User


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="deliver_addresses",
        blank=True,
        null=True
    )

    postcode = models.IntegerField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    building = models.IntegerField()
    body = models.IntegerField()
    flat = models.IntegerField()
    floor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Deliver address for {self.user}"
