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
