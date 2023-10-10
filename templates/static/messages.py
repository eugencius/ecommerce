from django.utils.translation import gettext_lazy as _

success = {
    "product_to_cart": _("You've added a new product to your cart!"),
    "product_cart_remove": _("You've removed an item from your cart!"),
    "registered_successfuly": _(
        "Now you're registered! Just login and be prepared to enjoy our site."
    ),
}

error = {
    "form_invalid": _("There are invalid fields in your form. Fix them and try again.")
}
