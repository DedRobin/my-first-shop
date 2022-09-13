from django.contrib import admin

from products.models import Product, FavoriteProduct


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "external_id", "link")
    search_fields = ("title", "external_id")


@admin.register(FavoriteProduct)
class FavoriteProductsAdmin(admin.ModelAdmin):
    list_display = ("user", "product")
    fields = ("user", "product")
    search_fields = ("user__email", "product__title")
