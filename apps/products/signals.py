import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from apps.products.models import Product


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except:
        pass


@receiver(pre_delete, sender=Product)
def delete_cover_after_delete(sender, instance, *args, **kwargs):
    delete_cover(instance)


@receiver(pre_save, sender=Product)
def delete_cover_if_unused(sender, instance, *args, **kwargs):
    old_instance = Product.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
