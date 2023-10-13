from collections import defaultdict

from allauth.account.forms import LoginForm as AllauthLoginForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from utils import functions

from .models import Address

User = get_user_model()


class LoginForm(AllauthLoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        captcha = ReCaptchaField(
            label="Captcha",
            widget=ReCaptchaV3(),
        )
        self.fields["captcha"] = captcha

        functions.add_attrs(self.fields["login"], "float", "form-floating mb-3")
        functions.add_attrs(self.fields["password"], "float", "form-floating mb-3")
        functions.add_attrs(self.fields["remember"], "float", "form-check text-start")

        functions.add_attrs(self.fields["login"], "class", "form-control")
        functions.add_attrs(self.fields["password"], "class", "form-control")
        functions.add_attrs(self.fields["remember"], "class", "form-check-input")


class SignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._form_errors = defaultdict(list)

        captcha = ReCaptchaField(
            label="Captcha",
            widget=ReCaptchaV3(),
        )
        self.fields["captcha"] = captcha

        functions.add_attrs(self.fields["email"], "col", "col-12")
        functions.add_attrs(self.fields["first_name"], "col", "col-md-6")
        functions.add_attrs(self.fields["last_name"], "col", "col-md-6")
        functions.add_attrs(self.fields["password1"], "col", "col-md-6")
        functions.add_attrs(self.fields["password2"], "col", "col-md-6")

        functions.set_placeholder(self.fields["email"], "Ex.: johndoe@gmail.com")
        functions.set_placeholder(self.fields["first_name"], "Ex.: John")
        functions.set_placeholder(self.fields["last_name"], "Ex.: Doe")
        functions.set_placeholder(
            self.fields["password1"], _("Please, type your password here.")
        )
        functions.set_placeholder(
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


fields = (
    "city",
    "state",
    "street",
    "number",
    "complement",
    "addressee",
    "cep",
    "cpf",
)


class CreateAddress(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = (
            ("city", _("Insert your city.")),
            ("state", _("Insert your state.")),
            ("street", _("Type your street.")),
            ("number", _("Put your house number here.")),
            ("complement", _("Inform the complement.")),
            ("addressee", _("Type the name of the addressee.")),
            ("cep", _("Insert the CEP of your address here.")),
            ("cpf", _("Insert your CPF here.")),
        )

        for field in fields:
            if field == "state":
                functions.add_attrs(self.fields[field], "class", "form-select")

            functions.add_attrs(self.fields[field], "class", "form-control")

        for field in fields[0:-2]:
            functions.add_attrs(self.fields[field], "col", "col-md-6")

        for field, placeholder in placeholders:
            functions.add_attrs(self.fields[field], "placeholder", placeholder)

    state = forms.ChoiceField(
        initial=("NN", "Escolha seu estado"),
        label=_("state"),
        choices=functions.brazil_states,
    )

    class Meta:
        model = Address
        fields = fields

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]

        is_valid = functions.validate_cpf(cpf)
        already_used = Address.objects.filter(cpf=cpf).exists()

        if not is_valid:
            raise ValidationError(_("The CPF you presented is not valid."))

        if already_used:
            raise ValidationError(
                _("The CPF you presented is already in use by another user.")
            )

        return cpf
