from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "price",
        "promotional_price",
        "stock",
        "updated_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_per_page = 25

    prepopulated_fields = {
        "slug": ("name",),
    }
