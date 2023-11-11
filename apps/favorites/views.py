from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View

from apps.products.models import Product
from templates.static import messages as notifications

from .models import FavoriteList, ItemFavorited

LOGIN_URL = "account_login"


class DisplayLists(LoginRequiredMixin, ListView):
    model = FavoriteList
    template_name = "favorites/list.html"
    context_object_name = "lists"
    login_url = LOGIN_URL

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(user=self.request.user).order_by("-id")

        return qs


class ListDetails(LoginRequiredMixin, View):
    login_url = LOGIN_URL
    template_name = "favorites/details.html"

    # TODO: -- Create an alternate manager for the query of items in lists

    def get(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        list_model = get_object_or_404(FavoriteList, pk=pk)
        items = ItemFavorited.objects.filter(favorites_list=list_model)

        self.context = {
            "list": list_model,
            "items": items,
        }

        return render(self.request, self.template_name, self.context)


class CreateList(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def post(self, *args, **kwargs):
        HTTP_REFERER = self.request.META.get("HTTP_REFERER", "products:index")

        name = self.request.POST.get("name")
        user = self.request.user

        FavoriteList.objects.create(
            user=user,
            name=name,
        )

        return redirect(HTTP_REFERER)


class DeleteList(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def post(self, *args, **kwargs):
        list_pk = self.kwargs.get("pk")

        (FavoriteList.objects.get(pk=list_pk)).delete()

        messages.success(self.request, notifications.success["list_deleted"])
        return redirect("favorites:lists")


class FavoriteItem(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        HTTP_REFERER = self.request.META.get("HTTP_REFERER")

        list_pk = self.kwargs.get("list_pk")
        product_pk = self.kwargs.get("product_pk")

        product = get_object_or_404(Product, pk=product_pk)
        favorites_list = get_object_or_404(FavoriteList, pk=list_pk)

        already_exists = ItemFavorited.objects.filter(
            favorites_list=favorites_list,
            product=product,
        ).exists()

        if already_exists:
            messages.error(self.request, notifications.error["already_favorited"])
            return redirect(HTTP_REFERER)

        ItemFavorited.objects.create(
            favorites_list=favorites_list,
            product=product,
        )

        messages.success(self.request, notifications.success["item_favorited"])
        return redirect(HTTP_REFERER)


class RemoveFromList(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        item_pk = self.kwargs.get("pk")
        item = get_object_or_404(ItemFavorited, pk=item_pk)

        list_pk = item.favorites_list.pk

        item.delete()
        return redirect("favorites:details", list_pk)
