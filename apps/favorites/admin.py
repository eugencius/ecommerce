from django.contrib import admin

from .models import FavoriteList, ItemFavorited


@admin.register(FavoriteList)
class FavoriteListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "slug", "created_at")


@admin.register(ItemFavorited)
class ItemFavoritedAdmin(admin.ModelAdmin):
    list_display = ("id", "favorites_list", "product", "created_at")
