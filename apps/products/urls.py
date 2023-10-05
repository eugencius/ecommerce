from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("details/<slug>/", views.Details.as_view(), name="details"),
    path("product/tocart/<pk>", views.ProductToCart.as_view(), name="to-cart"),
]
