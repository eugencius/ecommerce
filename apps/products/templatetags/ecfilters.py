from django import template

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
