from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import ListView, View

from apps.accounts.models import Address
from templates.static import messages as notifications
from utils.functions import cart_total_price, count_items_on_cart

from .models import Order, OrderItem


class VerifyCartMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("cart", None):
            messages.error(self.request, notifications.error["empty_cart"])
            return redirect("products:index")

        return super().dispatch(request, *args, **kwargs)


class ListOrders(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/list_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user).order_by("-id")

        return qs


class CheckoutView(LoginRequiredMixin, VerifyCartMixin, View):
    login_url = "account_login"
    template_name = "orders/checkout.html"

    def get(self, *args, **kwargs):
        addresses = Address.objects.filter(user=self.request.user)

        self.context = {
            "addresses": addresses,
            "BASE_DIR": settings.BASE_DIR,
        }

        return render(self.request, self.template_name, self.context)


class CreateOrder(LoginRequiredMixin, VerifyCartMixin, View):
    login_url = "account_login"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        return redirect("products:cart")

    def post(self, *args, **kwargs):
        cart = self.request.session.get("cart")

        total_price = cart_total_price(cart.values())
        total_items = count_items_on_cart(cart.values())
        shipping = int(self.request.POST.get("shipping"))
        address_id = self.request.POST.get("address")

        if shipping == "N/A":
            messages.error(self.request, notifications.error["invalid_shipping"])
            return redirect("orders:checkout")

        if address_id == "N/A":
            messages.error(self.request, notifications.error["invalid_address"])
            return redirect("orders:checkout")

        address = Address.objects.get(id=address_id)

        if shipping == 1:
            total_price += 10

        order = Order.objects.create(
            user=self.request.user,
            total_price=total_price,
            total_items=total_items,
            address=address,
            shipping=shipping,
        )

        order_items = OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    name=item["name"],
                    slug=item["slug"],
                    price=item["unit_price"],
                    promotional_price=item["unit_promotional_price"],
                    cover=item["cover"],
                    category=item["category"],
                    quantity=item["quantity"],
                )
                for item in self.request.session["cart"].values()
            ]
        )

        del self.request.session["cart"]
        messages.success(self.request, notifications.success["order_placed"])
        return redirect("products:index")
