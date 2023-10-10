import locale
import os

from django.conf import settings
from PIL import Image


def format_currency(value):
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    value = locale.currency(value, grouping=True, symbol=None)
    return value


def resize_image(image, new_width=800):
    img_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
    img_pil = Image.open(img_full_path)
    original_width, original_height = img_pil.size

    if original_width <= new_width:
        img_pil.close()
        return

    new_height = round(new_width * original_height / original_width)

    new_image = img_pil.resize((new_width, new_height), Image.LANCZOS)

    new_image.save(
        img_full_path,
        optimize=True,
        quality=60,
    )


def count_items_on_cart(cart):
    return sum([i["quantity"] for i in cart])


def cart_total_price(cart):
    return sum(
        [
            i["quant_promotional_price"]
            if i["quant_promotional_price"]
            else i["quant_price"]
            for i in cart
        ]
    )


def create_cart(self):
    if not self.request.session.get("cart"):
        self.request.session["cart"] = {}

    return self.request.session["cart"]


def add_attrs(field, attr, value):
    existing_attr = field.widget.attrs.get(attr, "")
    field.widget.attrs[attr] = f"{value} {existing_attr}"


def set_placeholder(field, placeholder):
    add_attrs(field, "placeholder", placeholder)
