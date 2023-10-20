from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city = models.CharField(_("city"), max_length=255)
    state = models.CharField(_("state"), max_length=255)
    street = models.CharField(_("street"), max_length=255)
    neighborhood = models.CharField(_("neighborhood"), max_length=255)
    number = models.CharField(_("number"), max_length=12)
    complement = models.CharField(
        _("complement"),
        max_length=64,
        blank=True,
        null=True,
        help_text=_("Ex.: House B, Apt. 76"),
    )
    addressee = models.CharField(_("addressee"), max_length=64)
    cep = models.CharField(
        max_length=8, help_text=_("Type the CEP without any punctuations.")
    )
    cpf = models.CharField(
        max_length=11,
        help_text=_("Type the CPF without any punctuations."),
        unique=True,
    )

    def __str__(self):
        return f"Address of {self.user}"
