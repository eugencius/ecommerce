from django.views.generic import DetailView, ListView

from .models import Product


class Index(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by("-id").filter(is_published=True)
        return qs


class Details(DetailView):
    model = Product
    template_name = "products/details.html"
    context_object_name = "product"
    slug_url_kwarg = "slug"
