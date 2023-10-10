from collections import defaultdict

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils.functions import add_attrs, set_placeholder

User = get_user_model()


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._form_errors = defaultdict(list)

        add_attrs(self.fields["email"], "col", "col-12")
        add_attrs(self.fields["first_name"], "col", "col-md-6")
        add_attrs(self.fields["last_name"], "col", "col-md-6")
        add_attrs(self.fields["password1"], "col", "col-md-6")
        add_attrs(self.fields["password2"], "col", "col-md-6")

        set_placeholder(self.fields["email"], "Ex.: johndoe@gmail.com")
        set_placeholder(self.fields["first_name"], "Ex.: John")
        set_placeholder(self.fields["last_name"], "Ex.: Doe")
        set_placeholder(self.fields["password1"], _("Please, type your password here."))
        set_placeholder(
            self.fields["password2"],
            _("We need you to confirm your password here."),
        )

    email = forms.EmailField(
        max_length=256,
        label="E-mail",
        required=True,
        error_messages={
            "required": _("Sorry, you must enter your e-mail."),
        },
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    first_name = forms.CharField(
        max_length=64,
        label=_("First name"),
        required=True,
        error_messages={
            "required": _("Sorry, you must enter your first name."),
        },
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    last_name = forms.CharField(
        max_length=64,
        label=_("Last name"),
        required=True,
        error_messages={
            "required": _("Sorry, you must enter your last name."),
        },
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    password1 = forms.CharField(
        max_length=255,
        label=_("Password"),
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        max_length=255,
        label=_("Confirm password"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True,
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def clean(self):
        data = super().clean()

        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password1")
        password2 = data.get("password2")

        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            self._form_errors["email"].append(
                _("This e-mail address is already being used by another user.")
            )

        if password != password2:
            self._form_errors["password1"].append(
                _("The both password fields must be equal.")
            )
            self._form_errors["password2"].append(
                _("The both password fields must be equal.")
            )

        if first_name == last_name:
            self._form_errors["last_name"].append(
                _("The last name can't be equal to the first name.")
            )

        if self._form_errors:
            raise ValidationError(self._form_errors)

    # def save(self):
    #     user = super().save()
    #     return user
