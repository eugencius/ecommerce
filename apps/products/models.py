from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=64)
    slug = models.SlugField(blank=True)
    short_description = models.CharField(
        verbose_name=_("Short description"), max_length=128
    )
    long_description = models.TextField(verbose_name=_("Long description"))
    price = models.FloatField(verbose_name=_("Price"))
    promotional_price = models.FloatField(
        verbose_name=_("Promotional price"), default=0
    )
    cover = models.ImageField(verbose_name=_("Cover"), upload_to="media/images/")
    stock = models.PositiveIntegerField(verbose_name=_("Stock"))
    is_published = models.BooleanField(verbose_name=_("Is published"), default=True)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = f"{slug}"

        super().save(*args, **kwargs)
