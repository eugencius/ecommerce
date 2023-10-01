from django.shortcuts import render
from django.views.generic import ListView

from .models import Product


class Index(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"
    paginate_by = 6
