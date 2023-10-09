from django.urls import reverse

from .product_test_base import ProductBaseTest


class TestRemoveFromCart(ProductBaseTest):
    def setUp(self):
        super().setUp()

        self.p001 = self.create_product(
            name="Product 001",
            price=1200,
            promotional_price=1000,
        )
        self.pk = str(self.p001.pk)

        self.product_to_cart_x_times(self.p001.pk, 5)

    def remove_from_cart(self, pk):
        url = reverse("products:remove-from-cart", args=(pk,))
        return self.client.post(url)

    def remove_from_cart_x_times(self, pk, times=2):
        for i in range(0, times):
            self.remove_from_cart(pk)

    def test_product_removed_from_session_if_quantity_equals_zero(self):
        cart = self.client.session["cart"]
        self.assertIn(self.pk, cart.keys())

        self.remove_from_cart_x_times(self.pk, 5)

        cart = self.client.session["cart"]
        self.assertFalse(cart)

    def test_product_quantity_decreases(self):
        cart = self.client.session["cart"]
        quantity = cart[self.pk]["quantity"]

        self.assertEqual(quantity, 5)

        # -----------------------------------
        self.remove_from_cart(self.pk)

        cart = self.client.session["cart"]
        quantity = cart[self.pk]["quantity"]

        self.assertEqual(quantity, 4)

    def test_product_price_decreases(self):
        cart = self.client.session["cart"]

        expected_price = 1200 * 5
        cart_price = cart[self.pk]["quant_price"]

        self.assertEqual(expected_price, cart_price)
        # ------------------------------------------
        self.remove_from_cart(self.pk)

        cart = self.client.session["cart"]

        expected_price = 1200 * 4
        cart_price = cart[self.pk]["quant_price"]

        self.assertEqual(expected_price, cart_price)

    def test_product_promotional_price_decreases(self):
        cart = self.client.session["cart"]

        expected_price = 1000 * 5
        cart_price = cart[self.pk]["quant_promotional_price"]

        self.assertEqual(expected_price, cart_price)
        # ------------------------------------------
        self.remove_from_cart(self.pk)

        cart = self.client.session["cart"]

        expected_price = 1000 * 4
        cart_price = cart[self.pk]["quant_promotional_price"]

        self.assertEqual(expected_price, cart_price)
