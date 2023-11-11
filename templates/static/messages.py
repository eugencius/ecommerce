from django.utils.translation import gettext_lazy as _

success = {
    "product_to_cart": _("You've added a new product to your cart!"),
    "product_cart_remove": _("You've removed an item from your cart!"),
    "registered_successfuly": _(
        "Now you're registered! Just login and be prepared to enjoy our site."
    ),
    "address_registered": _("You've registered a new address sucessfuly!"),
    "order_placed": _(
        "Your order was placed sucessfully! Thank you for trusting in our site."
    ),
    "item_favorited": _("You have saved this product successfuly!"),
    "list_deleted": _("You have deleted a list sucessfuly."),
}

error = {
    "invalid_credentials": _(
        "Invalid login credentials. Please check your e-mail and password and try again."
    ),
    "form_invalid": _("There are invalid fields in your form. Fix them and try again."),
    "captcha_invalid": _("The captcha validation failed. Please try again."),
    "empty_cart": _("Your cart is empty. Add items on it before placing an order."),
    "order_get": _("You have to click on the button here to place an order."),
    "invalid_shipping": _("The method of shipping chosen is not valid."),
    "invalid_address": _("The address chosen is not valid."),
    "already_favorited": _("This item is already favorited in this list."),
}

templates_messages = {
    "shop": _("Shop"),
    "all_products": _("All Products"),
    "t_shirt": _("T-Shirt"),
    "shipping": _("Shipping"),
    "cellphone": _("Cellphone"),
    "general": _("General"),
    "socialaccounts_exists": _(
        "An account already exists with this email address. Please sign in to that account first, then connect your %s account."
    ),
}
