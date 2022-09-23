from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "user", "first_name", "last_name", "patronymic", "phone_number", "social_network_link", "slug", "created_at")
    fields = (
        "user", "first_name", "last_name", "patronymic", "phone_number", "social_network_link", "slug")
    readonly_fields = ("created_at",)
    search_fields = (
        "user__email", "first_name", "last_name", "patronymic", "phone_number", "social_network_link", "slug",
        "created_at")
