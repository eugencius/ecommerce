from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("create/", views.CreateOrder.as_view(), name="create_order"),
    path("list/", views.ListOrders.as_view(), name="list_orders"),
]
