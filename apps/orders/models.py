from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Address

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    total_items = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipping = models.CharField(
        max_length=1,
        choices=(
            ("0", "Standard"),
            ("1", "Express"),
        ),
    )

    def __str__(self):
        return _("Order ") + f"#{self.pk}"

    def save(self, *args, **kwargs):
        self.total_price = round(self.total_price, 2)
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    short_description = models.CharField(max_length=128)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    cover = models.CharField(max_length=999)
    category = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return _("Item from the order ") + f"#{self.order.pk}"
