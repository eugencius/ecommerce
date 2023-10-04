from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    def ready(self, *args, **kwargs):
        import apps.products.signals

        super_ready = super().ready(*args, **kwargs)
        return super_ready
