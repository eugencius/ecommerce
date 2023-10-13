from django.urls import path

from . import views

urlpatterns = [
    path(
        "create/address/", views.CreateAddress.as_view(), name="account_create_address"
    ),
    path("signup/", views.SignupView.as_view(), name="account_signup"),
    path("login/", views.LoginView.as_view(), name="account_login"),
]
