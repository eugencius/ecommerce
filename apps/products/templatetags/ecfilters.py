from django import template
from django.utils.translation import gettext as _

from apps.favorites.models import ItemFavorited
from utils import functions

register = template.Library()


@register.filter(name="format_currency_template")
def format_currency_template(value):
    return f"R${functions.format_currency(value)}"


@register.filter(name="count_cart_items")
def count_cart_items(cart):
    return functions.count_items_on_cart(cart)


@register.filter(name="cart_total_price")
def cart_total_price(cart):
    return functions.cart_total_price(cart)


@register.filter(name="translate_template")
def translate_template(name):
    return str(_(name))


@register.filter(name="count_items_in_list")
def count_items_in_list(list_name):
    return ItemFavorited.objects.filter(favorites_list__name__exact=list_name).count()
