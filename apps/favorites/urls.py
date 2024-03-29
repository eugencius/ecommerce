from django.urls import path

from . import views

app_name = "favorites"

urlpatterns = [
    path("lists/", views.DisplayLists.as_view(), name="lists"),
    path("list/details/<pk>", views.ListDetails.as_view(), name="details"),
    path("list/create/", views.CreateList.as_view(), name="create_list"),
    path("list/delete/<pk>", views.DeleteList.as_view(), name="delete_list"),
    path(
        "list/item/remove/<pk>", views.RemoveFromList.as_view(), name="remove_from_list"
    ),
    path(
        "item/favorite/<int:list_pk>/<int:product_pk>",
        views.FavoriteItem.as_view(),
        name="favorite_item",
    ),
]
