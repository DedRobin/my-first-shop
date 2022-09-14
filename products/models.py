from django.db import models

from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=200)
    cost = models.DecimalField(decimal_places=2, max_digits=7)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # from scrapy
    external_id = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        User, related_name="favorites", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user}, {self.product.title}"


class Purchase(models.Model):
    user = models.ForeignKey(
        User, related_name="purchases", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, blank=True, null=True)
