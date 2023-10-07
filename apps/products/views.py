import json
from typing import Any

from django.contrib import messages
from django.db import models
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View

from templates.static import messages as notifications

from .models import Product


class Index(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by("-id").filter(is_published=True)
        return qs


class Details(DetailView):
    model = Product
    template_name = "products/details.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()

        category = context["product"].category
        related_products = Product.objects.filter(
            category__exact=category, is_published=True
        ).exclude(id=obj.id)

        context["related_products"] = related_products

        return context


class Cart(View):
    template_name = "products/cart.html"

    def get(self, *args, **kwargs):
        cart = self.request.session.get("cart")

        context = {
            "cart": cart.values(),
        }

        return render(self.request, self.template_name, context)


class ProductToCart(View):
    def post(self, *args, **kwargs):
        HTTP_REFERER = self.request.META.get("HTTP_REFERER")

        pk = self.kwargs.get("pk")
        product = Product.objects.get(pk=pk)

        if not self.request.session.get("cart"):
            self.request.session["cart"] = {}

        cart = self.request.session["cart"]

        if pk not in cart.keys():
            cart[pk] = {
                "id": pk,
                "name": product.name,
                "slug": product.slug,
                "unit_price": product.price,
                "unit_promotional_price": product.promotional_price,
                "quant_price": product.price,
                "quant_promotional_price": product.promotional_price,
                "cover": product.cover.url,
                "category": product.category.name,
                "quantity": 1,
            }

        elif pk in cart.keys():
            quantity = cart[pk]["quantity"]

            updated_values = {
                "quantity": quantity + 1,
                "quant_price": cart[pk]["unit_price"] * (quantity + 1),
                "quant_promotional_price": cart[pk]["unit_promotional_price"]
                * (quantity + 1),
            }

            cart[pk].update(updated_values)

        self.request.session["cart"] = cart

        messages.success(
            self.request,
            notifications.success["product_to_cart"],
        )
        return redirect(HTTP_REFERER)


class RemoveProductCart(View):
    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")

        if not self.request.session.get("cart"):
            self.request.session["cart"] = {}

        cart = self.request.session["cart"]
        quantity = cart[pk]["quantity"] - 1

        updated_values = {
            "quantity": quantity,
            "quant_price": cart[pk]["unit_price"] * (quantity),
            "quant_promotional_price": cart[pk]["unit_promotional_price"] * (quantity),
        }

        cart[pk].update(updated_values)

        if quantity == 0:
            cart.pop(pk)

        self.request.session["cart"] = cart

        messages.error(
            self.request,
            notifications.success["product_cart_remove"],
        )

        return redirect("products:cart")
