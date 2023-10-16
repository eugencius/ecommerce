from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "total_items", "shipping")
    list_display_links = ("id", "user")


admin.site.register(OrderItem)
