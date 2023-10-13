from django.utils.translation import gettext_lazy as _

success = {
    "product_to_cart": _("You've added a new product to your cart!"),
    "product_cart_remove": _("You've removed an item from your cart!"),
    "registered_successfuly": _(
        "Now you're registered! Just login and be prepared to enjoy our site."
    ),
    "address_registered": _("You've registered a new address sucessfuly!"),
}

error = {
    "invalid_credentials": _(
        "Invalid login credentials. Please check your e-mail and password and try again."
    ),
    "form_invalid": _("There are invalid fields in your form. Fix them and try again."),
    "captcha_invalid": _("The captcha validation failed. Please try again."),
}
