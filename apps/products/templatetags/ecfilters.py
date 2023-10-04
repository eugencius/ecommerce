from django import template

from utils.functions import format_currency

register = template.Library()


@register.filter(name="format_currency_template")
def format_currency_template(value):
    return f"R${format_currency(value)}"
