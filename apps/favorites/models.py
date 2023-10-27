from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product

User = get_user_model()


class FavoriteList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = str(slug)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Favorite List")
        verbose_name_plural = _("Lists of Favorites")


class ItemFavorited(models.Model):
    favorites_list = models.ForeignKey(FavoriteList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{_('Item favorited in the list')} {self.favorites_list.name}"

    class Meta:
        verbose_name = _("Item Favorited")
        verbose_name_plural = _("Favorited Items")
