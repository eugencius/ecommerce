from typing import Any

import requests
from allauth.account.views import LoginView as AllauthLoginView
from allauth.account.views import SignupView as AllauthSignupView
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import FormView

from templates.static import messages as notifications

from .forms import CreateAddress
from .models import Address


class SignupView(AllauthSignupView):
    def form_invalid(self, form):
        messages.error(self.request, notifications.error["form_invalid"])

        return super().form_invalid(form)

    def form_valid(self, form):
        password = self.request.POST.get("password1")

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        messages.success(
            self.request,
            notifications.success["registered_successfuly"],
        )
        return redirect("account_login")


class LoginView(AllauthLoginView):
    redirect_field_name = "next"

    def form_invalid(self, form):
        email = self.request.POST.get("login")
        password = self.request.POST.get("password")

        url = self.request.path
        request_next = self.request.POST.get("next", None)
        next_parameter = f"?next={request_next}" if request_next else ""

        redirect_url = f"{url}{next_parameter}"

        is_correct = authenticate(self.request, email=email, password=password)

        (
            messages.error(self.request, notifications.error["invalid_credentials"])
            if not is_correct
            else messages.error(self.request, notifications.error["captcha_invalid"])
        )

        return redirect(redirect_url)


class CreateAddress(LoginRequiredMixin, FormView):
    login_url = "account_login"
    form_class = CreateAddress
    template_name = "account/address_create.html"
    success_url = "/"

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user
        address.save()

        messages.success(self.request, notifications.success["address_registered"])
        return super().form_valid(form)
