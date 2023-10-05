import json

from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

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


class ProductToCart(View):
    def post(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        product = Product.objects.get(pk=pk)

        if not self.request.session.get("cart"):
            self.request.session["cart"] = {}

        cart = self.request.session["cart"]

        if pk not in cart.keys():
            cart[pk] = {
                "name": product.name,
                "slug": product.slug,
                "unit_price": product.price,
                "unit_promotional_price": product.promotional_price,
                "quant_price": product.price,
                "quant_promotional_price": product.promotional_price,
                "cover": product.cover.url,
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
        return redirect("products:details", product.slug)
