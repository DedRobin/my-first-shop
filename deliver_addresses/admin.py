from django.contrib import admin

from deliver_addresses.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "postcode", "country", "city", "street", "building", "body", "flat", "floor", "created_at")
    fields = ("user", "postcode", "country", "city", "street", "building", "body", "flat", "floor")
    readonly_fields = ("created_at",)
    search_fields = ("user__email", "postcode", "country", "city", "street", "building", "body", "flat", "floor")
