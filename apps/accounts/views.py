from allauth.account.views import SignupView as AllauthSignupView
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from templates.static import messages as notifications


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
