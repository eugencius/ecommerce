from django.urls import path

from . import views

app_name = "favorites"

urlpatterns = [
    path("create/", views.CreateList.as_view(), name="create_list"),
    path(
        "item/favorite/<int:list_pk>/<int:product_pk>",
        views.FavoriteItem.as_view(),
        name="favorite_item",
    ),
]
