from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View

from apps.products.models import Product
from templates.static import messages as notifications

from .models import FavoriteList, ItemFavorited


class DisplayLists(LoginRequiredMixin, ListView):
    model = FavoriteList
    template_name = "favorites/list.html"
    context_object_name = "lists"
    login_url = "account_login"

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(user=self.request.user).order_by("-id")

        return qs


class CreateList(LoginRequiredMixin, View):
    login_url = "account_login"

    def post(self, *args, **kwargs):
        HTTP_REFERER = self.request.META.get("HTTP_REFERER", "products:index")

        name = self.request.POST.get("name")
        user = self.request.user

        FavoriteList.objects.create(
            user=user,
            name=name,
        )

        return redirect(HTTP_REFERER)


class FavoriteItem(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        HTTP_REFERER = self.request.META.get("HTTP_REFERER")

        list_pk = self.kwargs.get("list_pk")
        product_pk = self.kwargs.get("product_pk")

        product = get_object_or_404(Product, pk=product_pk)
        favorites_list = get_object_or_404(FavoriteList, pk=list_pk)

        ItemFavorited.objects.create(
            favorites_list=favorites_list,
            product=product,
        )

        messages.success(self.request, notifications.success["item_favorited"])
        return redirect(HTTP_REFERER)
